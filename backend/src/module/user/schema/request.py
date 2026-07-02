from pydantic import field_validator

from src.core.schema import BaseRequest
from src.shared.util.validation import validate_password


class UserUpdateRequest(BaseRequest):
    full_name: str | None = None
    password: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str | None) -> str | None:
        if v is not None:
            errors = validate_password(v)
            if errors:
                raise ValueError("; ".join(errors))
        return v
