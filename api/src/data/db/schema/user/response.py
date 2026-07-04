from datetime import datetime

from src.core.schema import BaseResponse


class UserSchema(BaseResponse):
    id: str
    email: str
    username: str
    full_name: str | None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
