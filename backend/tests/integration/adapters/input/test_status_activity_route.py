from unittest.mock import patch

import pytest

# --- Fixtures ---

@pytest.fixture
def mock_repository_find_one():
    with patch(
        "src.adapters.output.activity_repository_mongo_adapter.ActivityRepositoryAdapter.find_one"
    ) as mock_find_one:
        yield mock_find_one

# --- Tests ---

@pytest.mark.asyncio
async def test_status_activity_success(
    async_client,
    mock_activity_fixture,
    mock_activity_document_fixture,
    mock_participant_regular,
    mock_participant_owner,
):
    # Given
    await mock_activity_document_fixture.insert()

    # When
    response = await async_client.get(
        f"/v1/activity/{mock_activity_fixture.id}",
        headers={"X-Participant-Id": str(mock_participant_regular.id)}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["activity"]["owner"]["id"] == str(mock_participant_owner.id)


@pytest.mark.asyncio
async def test_status_activity_not_found(
    async_client,
    mock_activity_fixture,
    mock_participant_regular,
):
    # When
    response = await async_client.get(
        f"/v1/activity/{mock_activity_fixture.id}",
        headers={"X-Participant-Id": str(mock_participant_regular.id)}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.text


@pytest.mark.asyncio
async def test_status_activity_unexpected_error(
    async_client,
    mock_activity_fixture,
    mock_participant_regular,
    mock_repository_find_one
):
    # Given
    mock_repository_find_one.side_effect = Exception("Database failure")

    # When
    response = await async_client.get(
        f"/v1/activity/{mock_activity_fixture.id}",
        headers={"X-Participant-Id": str(mock_participant_regular.id)}
    )

    # Assert
    assert response.status_code == 500
    assert "Unexpected error occurred" in response.text
