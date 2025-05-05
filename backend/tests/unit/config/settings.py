import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    logger.debug("[get_settings] Settings the database")

    env: str = "dev"
    log_level: str = "info"
    enable_profiling: bool = False
    allowed_origins: str = ""

    db_host: str = ""
    db_port: str = ""

    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    logger.debug("[get_settings] Settings initialized")


@lru_cache
def get_settings() -> Settings:
    return Settings()
