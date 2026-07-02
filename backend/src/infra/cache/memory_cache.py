import time

from src.infra.cache.base import BaseCache


class MemoryCache(BaseCache):
    def __init__(self):
        self._store: dict[str, tuple[str, float | None]] = {}

    async def _get_raw(self, key: str) -> str | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires = entry
        if expires is not None and time.time() > expires:
            del self._store[key]
            return None
        return value

    async def _set_raw(self, key: str, value: str, ttl: int | None = None) -> None:
        expires = (time.time() + ttl) if ttl else None
        self._store[key] = (value, expires)

    async def _delete_raw(self, key: str) -> None:
        self._store.pop(key, None)

    async def clear(self, prefix: str | None = None) -> None:
        if prefix:
            self._store = {k: v for k, v in self._store.items() if not k.startswith(prefix)}
        else:
            self._store.clear()
