from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.common import serialize
from src.core.type import Env


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: Env
    debug: bool
    log_format: str = "text"

    # DB
    db_schema: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: SecretStr

    # CORS
    cors_origins: str = ""

    # Auth
    jwt_secret: SecretStr
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Cache
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: SecretStr | None = None
    cache_ttl_default: int = 300

    # Observability
    metrics_enabled: bool = True

    @property
    def cors_origin_list(self) -> list[str]:
        if not self.cors_origins:
            return []
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def db_password_value(self) -> str:
        return serialize(self.db_password)

    @property
    def jwt_secret_value(self) -> str:
        return serialize(self.jwt_secret)


@lru_cache
def get_settings() -> Settings:
    return Settings()
