from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.config.config import get_settings
from src.core.error import Error
from src.core.security import JWT_ACCESS_TYPE, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_current_user_id(token: str | None = Depends(oauth2_scheme)) -> UUID | None:
    if not token:
        return None
    settings = get_settings()
    try:
        payload = decode_token(token, settings.jwt_secret_value, settings.jwt_algorithm, JWT_ACCESS_TYPE)
        return UUID(payload.sub)
    except Exception:
        return None


async def require_user_id(token: str | None = Depends(oauth2_scheme)) -> UUID:
    if not token:
        raise Error.unauthorized("Not authenticated")
    settings = get_settings()
    try:
        payload = decode_token(token, settings.jwt_secret_value, settings.jwt_algorithm, JWT_ACCESS_TYPE)
        return UUID(payload.sub)
    except Error:
        raise
    except Exception:
        raise Error.unauthorized("Invalid authentication token") from None
