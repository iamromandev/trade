from fastapi import APIRouter, Depends

from src.core.error import error_api_responses
from src.core.success import Success
from src.module.user.schema.request import UserUpdateRequest
from src.module.user.schema.response import UserSchema
from src.module.user.service.user_service import UserService
from src.shared.deps.auth import get_current_user_id

user_router = APIRouter(prefix="/user", tags=["users"])


@user_router.get("/me", responses=error_api_responses())
async def get_my_profile(
    service: UserService = Depends(UserService),
    user_id=Depends(get_current_user_id),
) -> Success[UserSchema]:
    result = await service.get_me(user_id=user_id)
    return Success.ok(data=result)


@user_router.patch("/me", responses=error_api_responses())
async def update_my_profile(
    body: UserUpdateRequest,
    service: UserService = Depends(UserService),
    user_id=Depends(get_current_user_id),
) -> Success[UserSchema]:
    result = await service.update_me(user_id=user_id, full_name=body.full_name, password=body.password)
    return Success.ok(data=result)
