from pydantic import EmailStr, field_validator

from src.core.schema import BaseRequest
from src.shared.util.validation import validate_password


class RegisterRequest(BaseRequest):
    email: EmailStr
    username: str
    password: str
    full_name: str | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not (3 <= len(v) <= 64):
            raise ValueError("Username must be between 3 and 64 characters")
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
        if not all(c in allowed for c in v):
            raise ValueError("Username may only contain alphanumeric chars, dots, underscores, and hyphens")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str) -> str:
        errors = validate_password(v)
        if errors:
            raise ValueError("; ".join(errors))
        return v


class LoginRequest(BaseRequest):
    username: str
    password: str


class RefreshRequest(BaseRequest):
    refresh_token: str
