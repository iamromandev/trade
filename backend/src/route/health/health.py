from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.error import error_api_responses
from src.core.success import Success
from src.data.db.schema.health.response import HealthSchema
from src.service.health import HealthService, get_health_service

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(path="/check", responses=error_api_responses())
async def health_check(
        service: Annotated[HealthService, Depends(get_health_service)]
) -> Success[HealthSchema]:
    result = await service.check()
    return Success.ok(data=result)
