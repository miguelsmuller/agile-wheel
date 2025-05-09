from unittest.mock import ANY

import pytest
from src.config.monitoring import initialize_monitoring
from src.config.settings import Settings


@pytest.fixture
def mock_sentry_sdk(mocker):
    return mocker.patch("src.config.monitoring.sentry_sdk")


@pytest.fixture
def mock_logger_info(mocker):
    return mocker.patch("src.config.monitoring.logger.info")


@pytest.fixture
def mock_settings():
    return Settings(
        env="testing",
        log_level="debug",
        enable_profiling=False,
        allowed_origins="*",
        db_host="localhost",
        db_port="27017",
        sentry_dns="https://fake-dsn.sentry.io/"
    )


def test_initialize_monitoring_successfully(
    mock_sentry_sdk,
    mock_logger_info,
    mock_settings
):
    initialize_monitoring(mock_settings)

    mock_sentry_sdk.init.assert_called_once_with(
        dsn=mock_settings.sentry_dns,
        environment=mock_settings.env,
        send_default_pii=True,
        integrations=[ANY],
    )

    mock_logger_info.assert_called_with("Sentry initialization successful")


def test_initialize_monitoring_fails(mock_sentry_sdk, mock_logger_info, mock_settings):
    mock_settings.sentry_dns = None

    initialize_monitoring(mock_settings)

    mock_sentry_sdk.init.assert_not_called()

    expected_log = "sentry_dsn not provided, skipping Sentry initialization"
    mock_logger_info.assert_called_once_with(expected_log)
