from dataclasses import replace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.application.usecase.get_activity_result_use_case import GetActivityResultService
from src.domain.entities.participant import Participant
from src.domain.exceptions import ActivityNotFoundError

ACTIVITY_ID = UUID("8e6587b8-b158-4068-a254-76bd0d31f4f7")
PARTICIPANT_ID = UUID("7870b158-4900-466a-948c-14b462b62f5b")
NON_MEMBER_ID = UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_activity_close(mock_activity_fixture):
    return replace(
        mock_activity_fixture,
        id=ACTIVITY_ID,
        is_opened=False,
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

@pytest.mark.asyncio
async def test_result_activity_success(mock_repository, mock_activity_close):
    # Given
    service = GetActivityResultService(repository=mock_repository)
    mock_repository.find_one.return_value = mock_activity_close

    # When
    result = await service.get_activity_result(activity_id=ACTIVITY_ID)

    # Then
    mock_repository.find_one.assert_awaited_once_with(ACTIVITY_ID)
    assert result.activity.id == ACTIVITY_ID
    assert result.activity.is_opened is False


@pytest.mark.asyncio
async def test_result_activity_not_found(mock_repository):
    # Given
    service = GetActivityResultService(repository=mock_repository)
    mock_repository.find_one.return_value = None

    # When & Then
    with pytest.raises(ActivityNotFoundError, match="Activity not found for update"):
        await service.get_activity_result(activity_id=ACTIVITY_ID)
