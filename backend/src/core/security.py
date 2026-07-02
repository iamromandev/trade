import uuid
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from src.core.error import Error
from src.core.schema import BaseSchema

JWT_ACCESS_TYPE = "access"
JWT_REFRESH_TYPE = "refresh"


class TokenPayload(BaseSchema):
    sub: str
    type: str
    iat: datetime
    exp: datetime
    jti: str


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def encode_token(subject: str, secret: str, algorithm: str, expires_in: int, token_type: str) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_token(token: str, secret: str, algorithm: str, expected_type: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise Error.expired_token() from None
    except jwt.InvalidTokenError:
        raise Error.invalid_token() from None

    if payload.get("type") != expected_type:
        raise Error.invalid_token()

    return TokenPayload(
        sub=payload["sub"],
        type=payload["type"],
        iat=datetime.fromtimestamp(payload["iat"], tz=UTC),
        exp=datetime.fromtimestamp(payload["exp"], tz=UTC),
        jti=payload["jti"],
    )
