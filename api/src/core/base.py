import uuid
from datetime import datetime
from uuid import UUID

from loguru import logger
from pydantic import BaseModel, ConfigDict
from tortoise import fields
from tortoise.models import Model

from src.core.mixin import BaseMixin


class Base(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        abstract = True

    async def soft_delete(self) -> None:
        self.deleted_at = datetime.utcnow()
        await self.save(update_fields=["deleted_at"])

    @classmethod
    def get_active(cls):
        return cls.filter(deleted_at__isnull=True)

    @classmethod
    def db_fields(cls) -> set[str]:
        return set(cls._meta.db_fields)

    @classmethod
    def from_query_result(cls, row) -> Base:
        return cls(**row)


class LinkBase(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BaseRepo[M: Model](BaseMixin):
    model: type[M]

    def __init__(self, model: type[M] | None = None):
        if model:
            self.model = model

    async def count(self, **filters) -> int:
        qs = self.model.get_active() if hasattr(self.model, "deleted_at") else self.model.all()
        if filters:
            qs = qs.filter(**filters)
        return await qs.count()

    async def first_by_raw(self, **filters) -> M | None:
        return await self.model.get_active().filter(**filters).first()

    async def exists(self, **filters) -> bool:
        return await self.model.get_active().filter(**filters).exists()

    async def get_or_create(self, defaults: dict | None = None, **kwargs) -> tuple[M, bool]:
        return await self.model.get_or_create(defaults=defaults or {}, **kwargs)

    async def create(self, **kwargs) -> M:
        return await self.model.create(**kwargs)

    async def get_or_none(self, **filters) -> M | None:
        return await self.model.get_active().filter(**filters).first()

    async def get_by_id(self, id: UUID) -> M | None:
        return await self.model.get_active().filter(id=id).first()

    async def get_ids(self, ids: list[UUID]) -> list[M]:
        return await self.model.get_active().filter(id__in=ids).all()

    async def get_one(self, **filters) -> M:
        return await self.model.get_active().get(**filters)

    async def get_many(self, **filters) -> list[M]:
        return await self.model.get_active().filter(**filters).all()

    async def get_paginated(
        self, page: int = 1, page_size: int = 20, order_by: list[str] | None = None, **filters
    ) -> tuple[list[M], int]:
        qs = self.model.get_active().filter(**filters)
        total = await qs.count()
        if order_by:
            qs = qs.order_by(*order_by)
        items = await qs.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    async def filter_existing_ids(self, ids: list[UUID]) -> set[UUID]:
        existing = await self.model.get_active().filter(id__in=ids).values_list("id", flat=True)
        return set(existing)

    async def bulk_create(self, objs: list[M]) -> list[M]:
        return await self.model.bulk_create(objs)

    async def update(self, id: UUID, **kwargs) -> M | None:
        obj = await self.get_by_id(id)
        if obj:
            await obj.update_from_dict(kwargs)
            await obj.save()
        return obj

    async def delete(self, id: UUID) -> bool:
        obj = await self.get_by_id(id)
        if obj:
            await obj.soft_delete()
            return True
        return False

    async def delete_by_filter(self, **filters) -> int:
        count = 0
        async for obj in self.model.get_active().filter(**filters):
            await obj.soft_delete()
            count += 1
        return count


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_dict(self) -> dict:
        return self.model_dump()

    def safe_dump(self) -> dict:
        return self.model_dump(mode="json")

    def log(self, level: str = "info") -> None:
        getattr(logger, level)(self.safe_dump())


class BaseService(BaseMixin):
    def __init__(self):
        logger.debug("{} instantiated", self._tag)
