from unittest.mock import patch

import pytest


@pytest.fixture
def mock_repository_find_one():
    with patch(
        "src.adapters.output.activity_repository_adapter.ActivityRepositoryAdapter.find_one"
    ) as mock_find_one:
        yield mock_find_one


@pytest.mark.asyncio
async def test_patch_join_activity_returns_200_and_participant_when_successful(
    async_client, mock_activity_document_fixture
):
    """Should return 200 and participant data when join activity succeeds."""

    # Given
    await mock_activity_document_fixture.insert()

    activity_id = mock_activity_document_fixture.app_id

    # When
    response = await async_client.patch(f"/v1/activity/{activity_id}/join", json={
        "participant": {
            "email": "test@example.com",
            "name": "Test User"
        }
    })

    # Then
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["participant"]["email"] == "test@example.com"
    assert response_data["participant"]["name"] == "Test User"

    assert "activity" in response_data
    assert response_data["activity"]["is_opened"] is True


@pytest.mark.asyncio
async def test_patch_join_activity_returns_404_when_activity_not_found(
    async_client, mock_uuid_string
):
    """Should return 404 when trying to join a non-existent activity."""

    # When
    response = await async_client.patch(f"/v1/activity/{mock_uuid_string}/join", json={
        "participant": {
            "email": "test@example.com",
            "name": "Test User"
        }
    })

    # Then
    assert response.status_code == 404
    assert "Activity not found" in response.text


@pytest.mark.asyncio
async def test_patch_join_activity_returns_500_on_unexpected_exception(
    async_client, mock_uuid_string, mock_repository_find_one
):
    """Should return 500 when an unexpected exception occurs during join."""

    # Given
    mock_repository_find_one.side_effect = Exception("Database failure")

    # When
    response = await async_client.patch(f"/v1/activity/{mock_uuid_string}/join", json={
        "participant": {
            "email": "test@example.com",
            "name": "Test User"
        }
    })

    # Then
    assert response.status_code == 500
    assert "Unexpected error occurred" in response.text
