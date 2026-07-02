from redis import asyncio as aioredis

from src.config.config import get_settings
from src.infra.cache.base import BaseCache


class RedisCache(BaseCache):
    def __init__(self):
        self._client: aioredis.Redis | None = None

    async def _get_client(self) -> aioredis.Redis:
        if self._client is None:
            settings = get_settings()
            self._client = aioredis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password.get_secret_value() if settings.redis_password else None,
                decode_responses=True,
            )
        return self._client

    async def _get_raw(self, key: str) -> str | None:
        client = await self._get_client()
        return await client.get(key)

    async def _set_raw(self, key: str, value: str, ttl: int | None = None) -> None:
        client = await self._get_client()
        if ttl:
            await client.setex(key, ttl, value)
        else:
            await client.set(key, value)

    async def _delete_raw(self, key: str) -> None:
        client = await self._get_client()
        await client.delete(key)

    async def exists(self, key: str) -> bool:
        client = await self._get_client()
        return await client.exists(key) > 0

    async def clear(self, prefix: str | None = None) -> None:
        client = await self._get_client()
        if prefix:
            cursor = 0
            while True:
                cursor, keys = await client.scan(cursor=cursor, match=f"{prefix}*")
                if keys:
                    await client.delete(*keys)
                if cursor == 0:
                    break
        else:
            await client.flushdb()

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
