from fastapi.responses import JSONResponse

from src.core.format import utc_iso_timestamp
from src.core.schema import BaseSchema, PaginationMeta
from src.core.type import Code, Status


class Success[T](BaseSchema):
    status: str = Status.SUCCESS
    code: int = Code.OK
    message: str | None = None
    data: T | None = None
    meta: PaginationMeta | None = None
    timestamp: str = ""

    def __init__(self, **data):
        if "timestamp" not in data:
            data["timestamp"] = utc_iso_timestamp()
        super().__init__(**data)

    @classmethod
    def new(
        cls, data: T | None = None, message: str | None = None, code: int = Code.OK, meta: PaginationMeta | None = None
    ) -> Success[T]:
        return cls(code=code, data=data, message=message, meta=meta)

    @classmethod
    def ok(cls, data: T | None = None, message: str | None = None) -> Success[T]:
        return cls(code=Code.OK, data=data, message=message)

    @classmethod
    def created(cls, data: T | None = None, message: str | None = "Created") -> Success[T]:
        return cls(code=Code.CREATED, data=data, message=message)

    @classmethod
    def no_content(cls, message: str | None = None) -> Success[T]:
        return cls(code=Code.NO_CONTENT, data=None, message=message)

    def to_resp(self) -> JSONResponse:
        return JSONResponse(status_code=self.code, content=self.model_dump())
