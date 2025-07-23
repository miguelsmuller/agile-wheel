from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import create_app, settings


@pytest.fixture
def mock_dependencies():
    with (
        patch("src.main.initialize_logger") as mock_logger,
        patch("src.main.initialize_database", new_callable=AsyncMock) as mock_init_db,
        patch.object(settings, "api_token", ""),
    ):
        yield mock_logger, mock_init_db


def test_create_app_initializes_properly(mock_dependencies):
    mock_logger, mock_init_db = mock_dependencies

    app = create_app()

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code in (200, 404)

        assert hasattr(app.state, "settings")
        assert app.state.settings.env

    mock_init_db.assert_awaited_once()
