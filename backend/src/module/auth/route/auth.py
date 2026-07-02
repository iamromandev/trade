from fastapi import APIRouter, Depends

from src.core.error import error_api_responses
from src.core.success import Success
from src.module.auth.schema.request import LoginRequest, RefreshRequest, RegisterRequest
from src.module.auth.schema.response import TokenSchema, UserSchema
from src.module.auth.service.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201, responses=error_api_responses())
async def register(body: RegisterRequest, service: AuthService = Depends(AuthService)) -> Success[UserSchema]:
    result = await service.register(
        email=body.email,
        username=body.username,
        password=body.password,
        full_name=body.full_name,
    )
    return Success.created(data=result)


@auth_router.post("/login", responses=error_api_responses())
async def login(body: LoginRequest, service: AuthService = Depends(AuthService)) -> Success[TokenSchema]:
    result = await service.authenticate(identifier=body.username, password=body.password)
    return Success.ok(data=result)


@auth_router.post("/refresh", responses=error_api_responses())
async def refresh(body: RefreshRequest, service: AuthService = Depends(AuthService)) -> Success[TokenSchema]:
    result = await service.refresh(refresh_token=body.refresh_token)
    return Success.ok(data=result)
