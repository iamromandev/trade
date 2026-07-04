from src.core.schema import BaseResponse


class HealthSchema(BaseResponse):
    version: str
    db: dict
