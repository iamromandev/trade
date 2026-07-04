from uuid import UUID

from src.core.base import BaseRepo
from src.data.db.model.user import User


class UserRepo(BaseRepo[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_or_none(email=email)

    async def get_by_username(self, username: str) -> User | None:
        return await self.get_or_none(username=username)

    async def get_by_id(self, id: UUID) -> User | None:
        return await self.get_or_none(id=id)

    async def email_exists(self, email: str) -> bool:
        return await self.exists(email=email)

    async def username_exists(self, username: str) -> bool:
        return await self.exists(username=username)
