from uuid import UUID

from loguru import logger

from src.core.base import BaseService
from src.core.error import Error
from src.core.jwt import JWTIssuer, jwt_issuer
from src.core.security import JWT_REFRESH_TYPE, decode_token, hash_password, verify_password
from src.data.db.repo.user_repo import UserRepo
from src.data.db.schema.auth.response import TokenSchema, UserSchema


class AuthService(BaseService):
    def __init__(self):
        super().__init__()
        self._repo = UserRepo()
        self._jwt: JWTIssuer = jwt_issuer

    async def register(self, email: str, username: str, password: str, full_name: str | None = None) -> UserSchema:
        if await self._repo.email_exists(email):
            raise Error.conflict("Email already registered")
        if await self._repo.username_exists(username):
            raise Error.conflict("Username already taken")

        user = await self._repo.create(
            email=email,
            username=username,
            hashed_password=hash_password(password),
            full_name=full_name,
        )
        logger.info("User registered: {} ({})", user.email, user.id)
        return UserSchema.model_validate(user)

    async def authenticate(self, identifier: str, password: str) -> TokenSchema:
        user = await self._repo.get_by_email(identifier) or await self._repo.get_by_username(identifier)
        if not user:
            raise Error.unauthorized("Invalid credentials")
        if not user.is_active:
            raise Error.unauthorized("Account is disabled")
        if not verify_password(password, user.hashed_password):
            raise Error.unauthorized("Invalid credentials")

        pair = self._jwt.issue_pair(str(user.id))
        logger.info("User logged in: {} ({})", user.email, user.id)
        return TokenSchema(
            access_token=pair.access_token,
            refresh_token=pair.refresh_token,
            expires_in=pair.expires_in,
        )

    async def refresh(self, refresh_token: str) -> TokenSchema:
        settings = await self._get_settings()
        payload = decode_token(refresh_token, settings.jwt_secret_value, settings.jwt_algorithm, JWT_REFRESH_TYPE)
        user = await self._repo.get_by_id(UUID(payload.sub))
        if not user or not user.is_active:
            raise Error.unauthorized("Invalid refresh token")
        pair = self._jwt.issue_pair(str(user.id))
        return TokenSchema(
            access_token=pair.access_token,
            refresh_token=pair.refresh_token,
            expires_in=pair.expires_in,
        )

    async def _get_settings(self):
        from src.config.config import get_settings

        return get_settings()
