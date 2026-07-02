from dataclasses import dataclass

from src.config.config import get_settings
from src.core.security import JWT_ACCESS_TYPE, JWT_REFRESH_TYPE, encode_token


@dataclass
class IssuedTokenPair:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class JWTIssuer:
    def __init__(self):
        self._settings = get_settings()

    def issue_access(self, user_id: str) -> str:
        return encode_token(
            subject=user_id,
            secret=self._settings.jwt_secret_value,
            algorithm=self._settings.jwt_algorithm,
            expires_in=self._settings.jwt_access_token_expire_minutes * 60,
            token_type=JWT_ACCESS_TYPE,
        )

    def issue_refresh(self, user_id: str) -> str:
        return encode_token(
            subject=user_id,
            secret=self._settings.jwt_secret_value,
            algorithm=self._settings.jwt_algorithm,
            expires_in=self._settings.jwt_refresh_token_expire_days * 86400,
            token_type=JWT_REFRESH_TYPE,
        )

    def issue_pair(self, user_id: str) -> IssuedTokenPair:
        access = self.issue_access(user_id)
        refresh = self.issue_refresh(user_id)
        return IssuedTokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=self._settings.jwt_access_token_expire_minutes * 60,
        )


jwt_issuer = JWTIssuer()
