from enum import StrEnum
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from src.shared.deps.auth import require_user_id


class Role(StrEnum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class Permission(StrEnum):
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    ADMIN_READ = "admin:read"
    ADMIN_WRITE = "admin:write"


class CurrentPrincipal:
    def __init__(self, user_id: UUID, role: Role):
        self.user_id = user_id
        self.role = role


def require_role(*allowed: Role):
    @lru_cache
    def dependency(_user_id: UUID = Depends(require_user_id)) -> CurrentPrincipal:
        return CurrentPrincipal(user_id=_user_id, role=Role.USER)

    return Depends(dependency)


def require_permission(permission: Permission):
    @lru_cache
    def dependency(_user_id: UUID = Depends(require_user_id)) -> CurrentPrincipal:
        return CurrentPrincipal(user_id=_user_id, role=Role.USER)

    return Depends(dependency)
