"""Application settings using Pydantic for env-based configuration."""

from __future__ import annotations

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurable environment-backed settings."""

    app_name: str = Field("MiniCRM API", description="Displayed application name")
    app_env: str = Field("local", description="Deployment environment identifier")
    debug: bool = Field(False, description="Enable debug mode")
    database_url: str = Field(..., env="DATABASE_URL", description="PostgreSQL DSN")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Singleton settings accessor."""

    return Settings()
