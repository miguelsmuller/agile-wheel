import logging
import os


def initialize_logger():
    log_level_env = os.getenv("LOG_LEVEL", "info").upper()
    log_level = getattr(logging, log_level_env, logging.INFO)

    logging.basicConfig(level=log_level)
    logging.debug("[init_logging] Logging initialized - level: %s", log_level_env)
