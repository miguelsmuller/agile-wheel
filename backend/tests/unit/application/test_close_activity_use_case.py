from dataclasses import replace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from src.application.usecase.close_activity_use_case import CloseActivityService


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.mark.asyncio
async def test_close_activity_success(mock_repository, mock_activity_fixture):
    # Given
    activity_data = replace(mock_activity_fixture, is_opened=True)

    mock_repository.find_one.return_value = activity_data
    mock_repository.update.return_value = activity_data

    service = CloseActivityService(repository=mock_repository)

    # When
    result = await service.execute(
        activity_id=activity_data.id,
        participant_id_requested=activity_data.participants[0].id
    )

    # Then
    mock_repository.find_one.assert_awaited_once_with(activity_data.id)
    mock_repository.update.assert_awaited_once_with(activity_data)
    assert result.is_opened is False


@pytest.mark.asyncio
async def test_close_activity_permission_error(mock_repository, mock_activity_fixture):
    # Given
    activity_data = replace(mock_activity_fixture, is_opened=True)
    mock_repository.find_one.return_value = activity_data

    service = CloseActivityService(repository=mock_repository)

    # When & Then
    with pytest.raises(PermissionError, match="Only the owner can close the activity"):
        await service.execute(
            activity_id=activity_data.id,
            participant_id_requested=UUID("3259afaa-29af-43ca-bcdd-3c52dfbfe2e7")
        )


@pytest.mark.asyncio
async def test_close_activity_not_found(mock_repository):
    # Given
    mock_repository.find_one.return_value = None

    service = CloseActivityService(repository=mock_repository)

    # When & Then
    with pytest.raises(ReferenceError, match="Activity not found for update"):
        await service.execute(
            activity_id=UUID("8e6587b8-b158-4068-a254-76bd0d31f4f7"),
            participant_id_requested=UUID("7870b158-4900-466a-948c-14b462b62f5b")
        )
