from dataclasses import replace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from src.application.usecase.join_activity_service import JoinActivityService
from src.domain.entities.participant import Participant

ACTIVITY_ID = UUID("8e6587b8-b158-4068-a254-76bd0d31f4f7")
NEW_PARTICIPANT_ID = UUID("7870b158-4900-466a-948c-14b462b62f5b")
NEW_PARTICIPANT_NAME = "Fulano da Silva"


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_activity(mock_activity_fixture):
    return replace(
        mock_activity_fixture,
        id=ACTIVITY_ID,
        is_opened=True,
        evaluations=[]
    )


@pytest.fixture
def mock_participant():
    return Participant(
        id=NEW_PARTICIPANT_ID,
        name=NEW_PARTICIPANT_NAME,
        role="regular",
        email="participant@example.com"
    )


@pytest.mark.asyncio
async def test_join_activity_success(mock_repository, mock_activity, mock_participant):
    # Given
    service = JoinActivityService(repository=mock_repository)
    mock_repository.find_one.return_value = mock_activity
    mock_repository.update.return_value = mock_activity

    # When
    result_activity, result_participant = await service.execute(
        activity_id=ACTIVITY_ID,
        participant=mock_participant
    )

    # Then
    mock_repository.find_one.assert_awaited_once_with(ACTIVITY_ID)
    mock_repository.update.assert_awaited_once_with(mock_activity)
    assert result_participant.id == mock_participant.id
    assert len(result_activity.participants) == 3
    assert result_activity.participants[2].id == mock_participant.id


@pytest.mark.asyncio
async def test_join_activity_not_found(mock_repository, mock_participant):
    # Given
    service = JoinActivityService(repository=mock_repository)
    mock_repository.find_one.return_value = None

    # When & Then
    with pytest.raises(
        AttributeError,
        match="'NoneType' object has no attribute 'add_participant'"
    ):
        await service.execute(activity_id=ACTIVITY_ID, participant=mock_participant)


@pytest.mark.asyncio
async def test_join_activity_repository_error(mock_repository, mock_activity, mock_participant):
    # Given
    service = JoinActivityService(repository=mock_repository)
    mock_repository.find_one.return_value = mock_activity
    mock_repository.update.side_effect = Exception("Erro ao atualizar atividade")

    # When & Then
    with pytest.raises(Exception, match="Erro ao atualizar atividade"):
        await service.execute(activity_id=ACTIVITY_ID, participant=mock_participant)
