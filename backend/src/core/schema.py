from pydantic import ConfigDict

from src.core.base import BaseSchema


class BaseRequest(BaseSchema):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class BaseResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseSchema):
    page: int
    page_size: int
    total: int
    total_pages: int

    @classmethod
    def build(cls, page: int, page_size: int, total: int) -> PaginationMeta:
        return cls(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=max(1, (total + page_size - 1) // page_size),
        )
