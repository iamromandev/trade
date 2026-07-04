import traceback

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from src.core.format import utc_iso_timestamp
from src.core.schema import BaseSchema
from src.core.type import Code, ErrorType, Status


class Violation(BaseSchema):
    field: str
    message: str


class ErrorDetail(BaseSchema):
    field: str
    message: str
    code: str


class ErrorResponse(BaseSchema):
    status: str = Status.ERROR
    code: int
    message: str
    type: str
    details: list[ErrorDetail] | None = None
    retry_able: bool = False
    timestamp: str = ""


class Error(Exception):
    def __init__(
        self,
        status: Status = Status.ERROR,
        code: Code = Code.INTERNAL_SERVER_ERROR,
        message: str = "Internal server error",
        type: ErrorType = ErrorType.INTERNAL_SERVER_ERROR,
        details: list[ErrorDetail] | None = None,
        retry_able: bool = False,
    ):
        self.status = status
        self.code = code
        self.message = message
        self.type = type
        self.details = details
        self.retry_able = retry_able
        self.timestamp = utc_iso_timestamp()

    @classmethod
    def bad_request(cls, message: str = "Bad request", details: list[ErrorDetail] | None = None) -> Error:
        return cls(code=Code.BAD_REQUEST, message=message, type=ErrorType.BAD_REQUEST, details=details)

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized") -> Error:
        return cls(code=Code.UNAUTHORIZED, message=message, type=ErrorType.UNAUTHORIZED)

    @classmethod
    def not_found(cls, message: str = "Resource not found") -> Error:
        return cls(code=Code.NOT_FOUND, message=message, type=ErrorType.NOT_FOUND)

    @classmethod
    def forbidden(cls, message: str = "Forbidden") -> Error:
        return cls(code=Code.FORBIDDEN, message=message, type=ErrorType.FORBIDDEN)

    @classmethod
    def conflict(cls, message: str = "Conflict") -> Error:
        return cls(code=Code.CONFLICT, message=message, type=ErrorType.CONFLICT)

    @classmethod
    def request_timeout(cls, message: str = "Request timeout") -> Error:
        return cls(code=Code.REQUEST_TIMEOUT, message=message, type=ErrorType.REQUEST_TIMEOUT)

    @classmethod
    def process_exception(cls, exc: Exception) -> Error:
        logger.error("Unhandled exception: {}", exc)
        logger.error(traceback.format_exc())
        return cls.process_validation_error()

    @classmethod
    def process_validation_error(cls) -> Error:
        return cls(code=Code.UNPROCESSABLE_ENTITY, message="Validation error", type=ErrorType.VALIDATION_ERROR)

    @classmethod
    def expired_token(cls) -> Error:
        return cls(code=Code.UNAUTHORIZED, message="Token has expired", type=ErrorType.EXPIRED_TOKEN)

    @classmethod
    def invalid_token(cls) -> Error:
        return cls(code=Code.UNAUTHORIZED, message="Invalid token", type=ErrorType.INVALID_TOKEN)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "type": self.type,
            "details": [d.model_dump() for d in self.details] if self.details else None,
            "retry_able": self.retry_able,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        import json

        return json.dumps(self.to_dict())

    def to_resp(self) -> JSONResponse:
        return JSONResponse(status_code=int(self.code), content=self.to_dict())


async def _http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    return Error(
        code=Code(exc.status_code),
        message=exc.detail,
        type=ErrorType.BAD_REQUEST if exc.status_code == 400 else ErrorType.INTERNAL_SERVER_ERROR,
    ).to_resp()


async def _validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        ErrorDetail(
            field=".".join(str(p) for p in err.get("loc", [])),
            message=err.get("msg", ""),
            code=err.get("type", ""),
        )
        for err in exc.errors()
    ]
    return Error.bad_request(message="Validation error", details=details).to_resp()


async def _error_handler(_request: Request, exc: Error) -> JSONResponse:
    return exc.to_resp()


async def _generic_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception: {}", exc)
    logger.error(traceback.format_exc())
    return Error.process_exception(exc).to_resp()


def init_global_errors(app):
    app.add_exception_handler(HTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)
    app.add_exception_handler(Error, _error_handler)
    app.add_exception_handler(Exception, _generic_exception_handler)


def error_api_responses() -> dict:
    return {
        400: {"description": "Bad Request", "model": ErrorResponse},
        401: {"description": "Unauthorized", "model": ErrorResponse},
        403: {"description": "Forbidden", "model": ErrorResponse},
        404: {"description": "Not Found", "model": ErrorResponse},
        422: {"description": "Validation Error", "model": ErrorResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse},
    }
