from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def mock_repository_create():
    with patch(
        "src.adapters.persistence.activity_repository_mongo_adapter.ActivityRepositoryAdapter.create"
    ) as mock_create:
        yield mock_create


@pytest.mark.asyncio
async def test_post_create_activity_returns_201_and_participant_on_success(async_client):
    """Should return 201 and participant data when activity is successfully created."""

    # Given
    payload = {
        "owner": {
            "email": "test@example.com",
            "name": "Test User"
        }
    }

    # When
    response = await async_client.post("/v1/activity", json=payload)


    # Then
    assert response.status_code == 201

    response_data = response.json()

    assert response_data["participant"]["email"] == "test@example.com"
    assert response_data["participant"]["name"] == "Test User"

    assert "activity" in response_data
    assert response_data["activity"]["is_opened"] is True


@pytest.mark.asyncio
async def test_post_create_activity_returns_500_on_unexpected_exception(mock_repository_create):
    """Should return 500 when an unexpected exception occurs during activity creation."""

    # Given
    client = TestClient(app)
    mock_repository_create.side_effect = Exception("Database failure")

    # When
    response = client.post("/v1/activity", json={
        "owner": {
            "email": "test@example.com",
            "name": "Test User"
        }
    })

    # Then
    assert response.status_code == 500
    assert "Unexpected error occurred" in response.text
