"""Seed the deployment's own data — run once per deployment, after ``scripts.migrate``.

``seed:default`` writes the SUPERADMIN account and nothing else. There is no default
password and no setting to fall back on: ``--password`` or a prompt on stdin supplies
it, so it stays out of source control, shell history and ``ps``. A re-run reuses the
account that exists and never changes its password.
"""

from __future__ import annotations

import argparse
import asyncio
import getpass
import sys

from loguru import logger
from src.core.error import Error
from src.core.security import hash_password
from src.data.db import DB_CONFIG
from src.data.db.repo.user_repo import UserRepo
from src.shared.util.validation import validate_password
from tortoise import Tortoise

SUPERADMIN_ROLE = "superadmin"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the deployment's SUPERADMIN account.")
    parser.add_argument("--email", required=True, help="address of the account")
    parser.add_argument("--username", help="handle; drawn from the local part of --email when omitted")
    parser.add_argument("--name", help="display name; drawn from the username when omitted")
    parser.add_argument("--password", help="omitted, prompted on stdin")
    return parser.parse_args(argv)


def read_password(given: str | None) -> str:
    if given:
        return given
    password = getpass.getpass("Password: ")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("passwords do not match")
    return password


async def seed_default(email: str, username: str | None, name: str | None, password: str | None) -> None:
    email = email.strip().lower()
    username = username or email.split("@", 1)[0]
    repo = UserRepo()

    if existing := await repo.get_by_email(email):
        logger.info("Superadmin {} already exists ({}); left as it is", existing.email, existing.id)
        return
    if await repo.username_exists(username):
        raise Error.conflict(f"Username {username!r} is taken; pass USERNAME=")

    secret = read_password(password)
    if errors := validate_password(secret):
        raise SystemExit("; ".join(errors))

    user = await repo.create(
        email=email,
        username=username,
        hashed_password=hash_password(secret),
        full_name=name or username,
        role=SUPERADMIN_ROLE,
        is_active=True,
    )
    logger.info("Seeded superadmin {} ({})", user.email, user.id)


async def run(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    await Tortoise.init(config=DB_CONFIG)
    try:
        await seed_default(args.email, args.username, args.name, args.password)
    finally:
        await Tortoise.close_connections()


def main() -> None:
    try:
        asyncio.run(run())
    except Error as error:
        sys.exit(error.message)


if __name__ == "__main__":
    main()
