from functools import lru_cache
import os
from pydantic import Field, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME")
    app_env: str = os.getenv("APP_ENV")
    debug: bool = False
    api_v1_prefix: str = os.getenv("API_V1_PREFIX")

    database_url: MySQLDsn

    jwt_secret: str = Field(min_length=32)
    jwt_refresh_secret: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    backend_cors_origins: list[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
