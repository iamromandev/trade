from functools import lru_cache

from src.infra.cache.memory_cache import MemoryCache


@lru_cache
def get_cache() -> MemoryCache:
    return MemoryCache()
