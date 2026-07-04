import asyncio

from src.core.security import hash_password
from src.data.db import run_migration
from src.data.db.repo.user_repo import UserRepo


async def seed():
    await run_migration()

    repo = UserRepo()

    existing = await repo.get_by_email("admin@example.com")
    if not existing:
        await repo.create(
            email="admin@example.com",
            username="admin",
            hashed_password=hash_password("Admin123456!"),
            full_name="Admin User",
            role="superadmin",
            is_active=True,
        )

    existing = await repo.get_by_email("user@example.com")
    if not existing:
        await repo.create(
            email="user@example.com",
            username="user",
            hashed_password=hash_password("User123456!"),
            full_name="Demo User",
            role="user",
            is_active=True,
        )


def main():
    asyncio.run(seed())


if __name__ == "__main__":
    main()
