from fastapi import APIRouter, Depends

from src.core.error import error_api_responses
from src.core.success import Success
from src.module.health.schema.response import HealthSchema
from src.module.health.service.health_service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(path="/check", responses=error_api_responses())
async def health_check(service: HealthService = Depends(HealthService)) -> Success[HealthSchema]:
    result = await service.check()
    return Success.ok(data=result)
