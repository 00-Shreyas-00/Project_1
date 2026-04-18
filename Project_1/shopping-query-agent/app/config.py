# shopping-query-agent/app/config.py
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and environment variables loaded from .env.
    """

    SERP_API_KEY: str = "dummy_serp_key"
    GOOGLE_API_KEY: str = "dummy_google_key"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
