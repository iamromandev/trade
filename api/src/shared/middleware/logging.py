import time
from typing import ClassVar

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    SKIP_PATHS: ClassVar[set[str]] = {"/metrics", "/health/check"}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        start = time.monotonic()
        response = await call_next(request)
        elapsed = (time.monotonic() - start) * 1000

        logger.info(
            "{} {} {} {:.0f}ms {}",
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
            request.headers.get("x-request-id", ""),
        )
        return response
