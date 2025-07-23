from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import create_app, settings


@pytest.fixture
def app_with_token(monkeypatch):
    settings.api_token = "secret-token"  # noqa: S105

    with (
        patch("src.main.initialize_logger"),
        patch("src.main.initialize_database", new_callable=AsyncMock),
        patch("src.main.initialize_monitoring"),
    ):
        app = create_app()
        yield app


def test_non_browser_without_token_returns_401(app_with_token):
    with TestClient(app_with_token) as client:
        response = client.get("/ping")
        assert response.status_code == 401


def test_non_browser_with_token_is_allowed(app_with_token):
    with TestClient(app_with_token) as client:
        headers = {"X-API-Token": "secret-token"}
        response = client.get("/ping", headers=headers)
        assert response.status_code == 200


def test_browser_request_allows_without_token(app_with_token):
    with TestClient(app_with_token) as client:
        headers = {"Origin": "http://example.com"}
        response = client.get("/ping", headers=headers)
        assert response.status_code == 200
