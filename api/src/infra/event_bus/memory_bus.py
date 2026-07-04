from collections import defaultdict

from loguru import logger

from src.infra.event_bus.base import BaseEventBus, EventHandler


class MemoryEventBus(BaseEventBus):
    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    async def publish(self, topic: str, data: dict) -> None:
        for handler in self._handlers.get(topic, []):
            try:
                await handler(data)
            except Exception as e:
                logger.error("Event handler failed on topic '{}': {}", topic, e)

    async def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._handlers[topic].append(handler)
        logger.debug("Subscribed to topic '{}'", topic)

    async def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        try:
            self._handlers[topic].remove(handler)
            logger.debug("Unsubscribed from topic '{}'", topic)
        except ValueError:
            pass
