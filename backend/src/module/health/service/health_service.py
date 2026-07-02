from loguru import logger

from src.core.base import BaseService
from src.core.common import get_app_version
from src.data.db import get_db_health, get_db_version
from src.module.health.schema.response import HealthSchema


class HealthService(BaseService):
    async def check(self) -> HealthSchema:
        db_ok = await get_db_health()
        db_version = await get_db_version() if db_ok else None

        logger.info("Health check: db={}", "up" if db_ok else "down")

        return HealthSchema(
            version=get_app_version(),
            db={
                "status": "healthy" if db_ok else "unhealthy",
                "version": db_version,
            },
        )
