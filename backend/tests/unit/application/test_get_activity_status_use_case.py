from dataclasses import replace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.application.usecase.get_activity_status_use_case import GetActivityStatusService
from src.domain.entities.participant import Participant

ACTIVITY_ID = UUID("8e6587b8-b158-4068-a254-76bd0d31f4f7")
PARTICIPANT_ID = UUID("7870b158-4900-466a-948c-14b462b62f5b")
NON_MEMBER_ID = UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_activity(mock_activity_fixture):
    return replace(
        mock_activity_fixture,
        id=ACTIVITY_ID,
        is_opened=True,
        participants=[
            Participant(
                id=PARTICIPANT_ID,
                name="Fulano da Silva",
                role="owner",
                email="owner@example.com"
            )
        ],
        evaluations=[]
    )

@pytest.fixture
def mock_activity_close(mock_activity):
    return replace(
        mock_activity,
        is_opened=False,
    )


@pytest.mark.asyncio
async def test_status_activity_success(mock_repository, mock_activity):
    # Given
    service = GetActivityStatusService(repository=mock_repository)
    mock_repository.find_one.return_value = mock_activity

    # When
    result = await service.get_activity_status(
        activity_id=ACTIVITY_ID, participant_id=PARTICIPANT_ID
    )

    # Then
    mock_repository.find_one.assert_awaited_once_with(ACTIVITY_ID)
    assert result.id == ACTIVITY_ID
    assert result.is_opened is True


@pytest.mark.asyncio
async def test_status_activity_not_found(mock_repository):
    # Given
    service = GetActivityStatusService(repository=mock_repository)
    mock_repository.find_one.return_value = None

    # When & Then
    with pytest.raises(ReferenceError, match="Activity not found for update"):
        await service.get_activity_status(activity_id=ACTIVITY_ID, participant_id=PARTICIPANT_ID)


@pytest.mark.asyncio
async def test_status_activity_permission_error(mock_repository, mock_activity):
    # Given
    service = GetActivityStatusService(repository=mock_repository)
    mock_repository.find_one.return_value = mock_activity

    # When & Then
    with pytest.raises(PermissionError, match="Only the members cant get the status"):
        await service.get_activity_status(activity_id=ACTIVITY_ID, participant_id=NON_MEMBER_ID)
