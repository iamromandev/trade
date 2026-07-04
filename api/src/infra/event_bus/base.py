from collections.abc import Awaitable, Callable

EventHandler = Callable[..., Awaitable[None]]


class BaseEventBus:
    async def publish(self, topic: str, data: dict) -> None:
        raise NotImplementedError

    async def subscribe(self, topic: str, handler: EventHandler) -> None:
        raise NotImplementedError

    async def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        raise NotImplementedError
