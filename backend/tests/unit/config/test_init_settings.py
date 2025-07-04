from unittest.mock import patch

import pytest

from src.config.settings import Settings, initialize_settings


@pytest.fixture
def mock_dependencies():
    with patch("src.config.settings.logger") as mock:
        yield mock


def test_get_settings_logs_and_return_type(mock_dependencies):
    # When
    initialize_settings.cache_clear()  # Clear lru_cache
    settings = initialize_settings()

    # Then
    assert isinstance(settings, Settings)

    assert mock_dependencies.debug.call_count >= 2

    log_messages = [call.args[0] for call in mock_dependencies.debug.call_args_list]
    assert "[GET_SETTINGS] Settings initialized" in log_messages
    assert "[GET_SETTINGS] Initializing settings" in log_messages
