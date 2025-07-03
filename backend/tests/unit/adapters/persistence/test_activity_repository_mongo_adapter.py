from dataclasses import replace
from unittest.mock import AsyncMock, patch

import pytest

from src.adapters.persistence.activity_document import ActivityDocumentForMongo
from src.adapters.persistence.activity_repository_mongo_adapter import ActivityRepositoryAdapter


@pytest.fixture
def mock_insert():
    with patch.object(ActivityDocumentForMongo, "insert", new_callable=AsyncMock) as mock_insert:
        yield mock_insert


@pytest.mark.asyncio
async def test_create_activity(mock_insert, mock_activity_fixture):
    # Given
    activity_data = mock_activity_fixture
    adapter = ActivityRepositoryAdapter()

    mock_insert.return_value = None

    # When
    result = await adapter.create(activity_data)

    # Then
    mock_insert.assert_awaited_once()
    assert result.id == activity_data.id
    assert result.created_at == activity_data.created_at
    assert result.is_opened == activity_data.is_opened


@pytest.mark.asyncio
async def test_create_activity_insert_error(mock_insert, mock_activity_fixture):
    # Given
    activity_data = mock_activity_fixture
    adapter = ActivityRepositoryAdapter()

    mock_insert.side_effect = Exception("Erro na inserção do documento")

    # When & Then
    with pytest.raises(Exception, match="Erro na inserção do documento"):
        await adapter.create(activity_data)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "missing_field, expected_error_message",
    [
        ("id", "badly formed hexadecimal UUID string"),
    ],
)
async def test_create_activity_missing_required_field(
    mock_activity_fixture,
    missing_field,
    expected_error_message
):
    # Given
    activity_data = replace(mock_activity_fixture, **{missing_field: None})
    adapter = ActivityRepositoryAdapter()

    # When & Then
    with pytest.raises(ValueError, match=expected_error_message):
        await adapter.create(activity_data)
