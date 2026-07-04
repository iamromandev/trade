from collections.abc import AsyncGenerator

from src.service.user.user_service import UserService


async def get_user_service() -> AsyncGenerator[UserService]:
    yield UserService()
