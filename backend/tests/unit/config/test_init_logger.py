import io
import logging

import pytest
from pythonjsonlogger.json import JsonFormatter
from src.config.logger import initialize_logger


@pytest.mark.parametrize("log_level_env, expected_level", [
    ("DEBUG", logging.DEBUG),
    ("INFO", logging.INFO),
    ("WARNING", logging.WARNING),
    ("ERROR", logging.ERROR),
    ("", logging.INFO),
])
def test_init_logging_sets_correct_level(monkeypatch, log_level_env, expected_level):
    # Given
    monkeypatch.setenv("LOG_LEVEL", log_level_env)

    logger = logging.getLogger()
    logger.handlers.clear()

    # When
    initialize_logger()

    # Then
    assert logger.level == expected_level

    assert len(logger.handlers) == 1
    handler = logger.handlers[0]

    # Check if the correct formatter is being used
    assert isinstance(handler.formatter, JsonFormatter)
    # Check if the handler is a StreamHandler
    assert isinstance(handler, logging.StreamHandler)


def test_initialize_logger_outputs_json(monkeypatch, capsys):
    # Given
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    log_stream = io.StringIO()

    logger = logging.getLogger()
    logger.handlers.clear()

    # When
    initialize_logger(stream=log_stream)

    logger = logging.getLogger()
    logger.debug("test message", extra={"foo": "bar"})

    # Logging handlers may buffer log messages before
    # writing them to the underlying stream. Calling
    # flush() ensures all log output is written to the
    # stream before reading its contents.
    for handler in logger.handlers:
        handler.flush()

    # Then
    log_contents = log_stream.getvalue()

    assert '"foo": "bar"' in log_contents
    assert "test message" in log_contents
