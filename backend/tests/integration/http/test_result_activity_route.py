from http import HTTPStatus
from unittest.mock import patch

import pytest

# --- Fixtures ---

@pytest.fixture
def mock_repository_find_one():
    with patch(
        "src.adapters.persistence.activity_repository_mongo_adapter.ActivityRepositoryAdapter.find_one"
    ) as mock_find_one:
        yield mock_find_one

# --- Tests ---

@pytest.mark.asyncio
async def test_result_activity_success(
    async_client,
    mock_activity_fixture,
    mock_activity_document_fixture,
):
    # Given
    await mock_activity_document_fixture.insert()

    # When
    response = await async_client.get(
        f"/v1/activity/{mock_activity_fixture.id}/result",
    )

    # Assert
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body["activity"]["activity_id"] == str(mock_activity_fixture.id)

    result = body.get("result")
    assert result is not None, "'result' must be present in the response"

    mandatory_result_keys = {"overall_score", "dimension_scores"}
    assert mandatory_result_keys.issubset(result), "missing keys in 'result'"

    dim_scores = result.get("dimension_scores")
    assert isinstance(dim_scores, list) and dim_scores, (
        "'dimension_scores' must be a non-empty list"
    )


@pytest.mark.asyncio
async def test_result_activity_not_found(
    async_client,
    mock_activity_fixture
):
    # When
    response = await async_client.get(
        f"/v1/activity/{mock_activity_fixture.id}/result",
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.text


@pytest.mark.asyncio
async def test_status_activity_unexpected_error(
    async_client,
    mock_activity_fixture,
    mock_repository_find_one
):
    # Given
    mock_repository_find_one.side_effect = Exception("Database failure")

    # When
    response = await async_client.get(
        f"/v1/activity/{mock_activity_fixture.id}/result",
    )

    # Assert
    assert response.status_code == 500
    assert "Unexpected error occurred" in response.text
