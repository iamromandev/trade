from functools import lru_cache

from src.infra.event_bus.memory_bus import MemoryEventBus


@lru_cache
def get_event_bus() -> MemoryEventBus:
    return MemoryEventBus()
