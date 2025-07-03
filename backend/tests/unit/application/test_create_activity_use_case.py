from dataclasses import replace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from src.application.usecase.create_activity_use_case import CreateActivityService
from src.domain.entities.participant import Participant

PARTICIPANT_ID = UUID("7870b158-4900-466a-948c-14b462b62f5b")
PARTICIPANT_NAME = "Fulano da Silva"

@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_owner():
    return Participant(
        id=PARTICIPANT_ID,
        name=PARTICIPANT_NAME,
        role="owner",
        email="owner@example.com"
    )

@pytest.fixture
def mock_activity(mock_activity_fixture, mock_owner):
    return replace(
        mock_activity_fixture,
        is_opened=True,
        participants=[mock_owner],
        evaluations=[]
    )



@pytest.mark.asyncio
async def test_create_activity_success(mock_repository, mock_owner, mock_activity):
    # Given
    service = CreateActivityService(repository=mock_repository)

    mock_repository.create.return_value = mock_activity

    # When
    result = await service.execute(owner=mock_owner)

    # Then
    mock_repository.create.assert_awaited_once()
    assert result.is_opened is True
    assert len(result.participants) == 1
    assert result.participants[0].id == mock_owner.id
    assert len(result.dimensions) > 0


@pytest.mark.asyncio
async def test_create_activity_repository_error(mock_repository, mock_owner):
    # Given
    service = CreateActivityService(repository=mock_repository)
    mock_repository.create.side_effect = Exception("Erro ao criar atividade")

    # When & Then
    with pytest.raises(Exception, match="Erro ao criar atividade"):
        await service.execute(owner=mock_owner)
