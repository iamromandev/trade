from uuid import UUID

from src.core.base import BaseService
from src.core.error import Error
from src.core.security import hash_password
from src.data.db.repo.user_repo import UserRepo
from src.module.user.schema.response import UserSchema


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self._repo = UserRepo()

    async def get_me(self, user_id: UUID) -> UserSchema:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise Error.not_found("User not found")
        return UserSchema.model_validate(user)

    async def update_me(self, user_id: UUID, full_name: str | None = None, password: str | None = None) -> UserSchema:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise Error.not_found("User not found")
        updates = {}
        if full_name is not None:
            updates["full_name"] = full_name
        if password is not None:
            updates["hashed_password"] = hash_password(password)
        if updates:
            user = await self._repo.update(user_id, **updates)
        return UserSchema.model_validate(user)
