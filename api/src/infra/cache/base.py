from abc import abstractmethod

from loguru import logger


class BaseCache:
    async def get(self, key: str) -> str | None:
        raw = await self._get_raw(key)
        if raw is not None:
            logger.trace("Cache HIT  key={}", key)
        else:
            logger.trace("Cache MISS key={}", key)
        return raw

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        logger.trace("Cache SET  key={}  ttl={}", key, ttl)
        await self._set_raw(key, value, ttl)

    async def delete(self, key: str) -> None:
        logger.trace("Cache DEL  key={}", key)
        await self._delete_raw(key)

    async def exists(self, key: str) -> bool:
        val = await self._get_raw(key)
        return val is not None

    async def clear(self, prefix: str | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _get_raw(self, key: str) -> str | None: ...

    @abstractmethod
    async def _set_raw(self, key: str, value: str, ttl: int | None = None) -> None: ...

    @abstractmethod
    async def _delete_raw(self, key: str) -> None: ...
