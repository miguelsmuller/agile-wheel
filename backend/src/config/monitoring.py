import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from src.config.settings import Settings

logger = logging.getLogger(__name__)


async def initialize_monitoring(settings: Settings):
    if settings.sentry_dns:
        logger.debug("Initializing Sentry")
        sentry_sdk.init(
            dsn=settings.sentry_dns,
            environment=settings.env,
            send_default_pii=True,
            integrations=[
                LoggingIntegration(level=logging.DEBUG, event_level=logging.FATAL),
            ],
        )
        logger.debug("[init_monitoring] Sentry initialization successful")
    else:
        logger.debug("[init_monitoring] Skipping Sentry initialization")
