import logging
import os
from unittest.mock import patch

import pytest
from src.config.logger import init_logger


@pytest.fixture
def mock_dependencies():
    with (
        patch("src.config.logger.logging.basicConfig") as mock_basic_config,
        patch("src.config.logger.logging.debug") as mock_debug
    ):
        yield mock_basic_config, mock_debug


@pytest.mark.parametrize("log_level_env, expected_level", [
    ("DEBUG", logging.DEBUG),
    ("INFO", logging.INFO),
    ("WARNING", logging.WARNING),
    ("ERROR", logging.ERROR),
    ("", logging.INFO),
])
def test_init_logging_sets_correct_level(log_level_env, expected_level, mock_dependencies):
    mock_basic_config, mock_debug = mock_dependencies

    with patch.dict(os.environ, {"LOG_LEVEL": log_level_env}):
        init_logger()

        mock_basic_config.assert_called_once_with(level=expected_level)
        mock_debug.assert_called_once_with(
            "[init_logging] Logging initialized - level: %s", log_level_env.upper()
        )
