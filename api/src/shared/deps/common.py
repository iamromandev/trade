from dataclasses import dataclass

from fastapi import Query


@dataclass
class PaginationParams:
    page: int = 1
    page_size: int = 20


@dataclass
class SortParams:
    sort: str = "-created_at"


async def pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)


async def sort_params(
    sort: str = Query("-created_at", description="Sort field(s), prefix with - for descending"),
) -> SortParams:
    return SortParams(sort=sort)
