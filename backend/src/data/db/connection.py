import asyncio
import random

from loguru import logger
from tortoise import Tortoise


async def wait_for_db(max_retries: int = 10) -> None:
    for attempt in range(1, max_retries + 1):
        try:
            conn = Tortoise.get_connection("default")
            await conn.execute_query("SELECT 1")
            logger.info("DB connection established")
            return
        except Exception as e:
            if attempt < max_retries:
                delay = min(2**attempt + random.uniform(0, 1), 15)
                logger.warning(
                    "DB connect attempt {}/{} failed: {}; retrying in {:.1f}s", attempt, max_retries, e, delay
                )
                await asyncio.sleep(delay)
            else:
                logger.error("DB connection failed after {} attempts", max_retries)
                raise


async def get_pool_stats() -> dict:
    try:
        conn = Tortoise.get_connection("default")
        pool = conn._pool
        return {
            "minsize": pool._minsize,
            "maxsize": pool._maxsize,
            "size": pool.size(),
            "free": pool.freesize if hasattr(pool, "freesize") else 0,
        }
    except Exception:
        return {}


async def close_all() -> None:
    await Tortoise.close_connections()
    logger.info("DB connections closed")
