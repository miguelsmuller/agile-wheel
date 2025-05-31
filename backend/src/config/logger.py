import logging
import os

from pythonjsonlogger.json import JsonFormatter


def initialize_logger(stream=None):
    log_level_env = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_env, logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = JsonFormatter()

    log_handler = logging.StreamHandler(stream)
    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)

    logging.debug("[init_logging] Logging initialized - level: %s", log_level_env)

    logging.getLogger("pymongo").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
