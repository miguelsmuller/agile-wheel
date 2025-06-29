from dataclasses import replace
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from src.application.usecase.evaluation_activity_use_case import EvaluationActivityService
from src.domain.entities.evaluation import ParticipantEvaluation, Rating

ACTIVITY_ID = UUID("8e6587b8-b158-4068-a254-76bd0d31f4f7")
PARTICIPANT_ID = UUID("7870b158-4900-466a-948c-14b462b62f5b")


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
def mock_evaluation():
    return ParticipantEvaluation(
        participant_id=PARTICIPANT_ID,
        ratings=[
            Rating(
                principle_id="compartilhamento_de_conhecimento",
                score=8.0,
                comments="",
            ),
            Rating(
                principle_id="comprometimento_com_o_produto",
                score=9.72,
                comments=None,
            )
        ]
    )


@pytest.mark.asyncio
async def test_evaluation_activity_success(mock_repository, mock_activity, mock_evaluation):
    # Given
    service = EvaluationActivityService(repository=mock_repository)
    mock_repository.find_one.return_value = mock_activity
    mock_repository.update.return_value = mock_activity

    # When
    result = await service.execute(activity_id=ACTIVITY_ID, evaluation=mock_evaluation)

    # Then
    mock_repository.find_one.assert_awaited_once_with(ACTIVITY_ID)
    mock_repository.update.assert_awaited_once_with(mock_activity)
    assert result.id == mock_evaluation.id
    assert result.participant_id == mock_evaluation.participant_id


@pytest.mark.asyncio
async def test_evaluation_activity_not_found(mock_repository, mock_evaluation):
    # Given
    service = EvaluationActivityService(repository=mock_repository)
    mock_repository.find_one.return_value = None

    # When & Then
    with pytest.raises(
        AttributeError,
        match="'NoneType' object has no attribute 'add_evaluation'"
    ):
        await service.execute(activity_id=ACTIVITY_ID, evaluation=mock_evaluation)


@pytest.mark.asyncio
async def test_evaluation_activity_repository_error(
    mock_repository,
    mock_activity,
    mock_evaluation
):
    # Given
    service = EvaluationActivityService(repository=mock_repository)
    mock_repository.find_one.return_value = mock_activity
    mock_repository.update.side_effect = Exception("Erro ao atualizar atividade")

    # When & Then
    with pytest.raises(Exception, match="Erro ao atualizar atividade"):
        await service.execute(activity_id=ACTIVITY_ID, evaluation=mock_evaluation)
