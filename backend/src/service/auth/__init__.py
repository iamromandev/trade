from collections.abc import AsyncGenerator

from src.service.auth.auth_service import AuthService


async def get_auth_service() -> AsyncGenerator[AuthService]:
    yield AuthService()



