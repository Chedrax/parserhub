from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "production"]

PROJECT_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    environment: Environment
    database_url: str
    secret_key: SecretStr
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
