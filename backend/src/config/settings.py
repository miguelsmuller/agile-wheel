import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

class Settings(BaseSettings):

    env: str = "LOCAL"
    log_level: str = "INFO"
    enable_profiling: bool = False
    enable_docs: bool = False
    allowed_origins: str = ""
    api_token: str = ""

    db_type: str = ""
    db_host: str = ""
    db_port: str = ""

    sentry_dns: str = ""

    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.debug("[GET_SETTINGS] Settings initialized")


@lru_cache
def initialize_settings() -> Settings:
    logger.debug("[GET_SETTINGS] Initializing settings")
    return Settings()
