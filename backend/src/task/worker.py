from dataclasses import dataclass

from src.config.config import get_settings


@dataclass
class WorkerSettings:
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    poll_delay: float = 3.0
    max_jobs: int = 10
    burst: bool = False


async def run_worker() -> None:
    settings = get_settings()
    ws = WorkerSettings(
        redis_host=settings.redis_host,
        redis_port=settings.redis_port,
        redis_db=settings.redis_db,
    )
    # ARQ worker would be initialised here:
    # worker = arq.ArqRedis(connection_settings=...)
    # await worker.run()
    _ = ws


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_worker())
