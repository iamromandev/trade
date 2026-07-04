from tortoise import fields

from src.core.base import Base


class User(Base):
    email = fields.CharField(max_length=255, unique=True, index=True)
    username = fields.CharField(max_length=64, unique=True, index=True)
    hashed_password = fields.CharField(max_length=255)
    full_name = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=32, default="user")
    is_active = fields.BooleanField(default=True)
    last_login_at = fields.DatetimeField(null=True)

    class Meta:
        table = "user"
