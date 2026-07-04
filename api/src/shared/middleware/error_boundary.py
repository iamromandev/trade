import traceback

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class ErrorBoundaryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            logger.error("Unhandled exception: {}", exc)
            logger.error(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "code": 500,
                    "message": "Internal server error",
                    "type": "internal_server_error",
                    "details": None,
                    "retry_able": False,
                    "timestamp": None,
                },
            )
