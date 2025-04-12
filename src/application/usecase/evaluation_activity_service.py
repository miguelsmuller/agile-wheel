from typing import TYPE_CHECKING
from uuid import UUID

from src.application.ports.input.evaluation_activity_port import EvaluationActivityPort
from src.domain.entities.evaluation import ParticipantEvaluation

if TYPE_CHECKING:
    from src.application.ports.output.activity_repository import ActivityRepositoryPort


class EvaluationActivityService(EvaluationActivityPort):

    def __init__(self, repository = None):
        self.repository: ActivityRepositoryPort = repository

    async def execute(
        self,
        activity_id: UUID,
        evaluation: ParticipantEvaluation
    ) -> ParticipantEvaluation:
        activity = await self.repository.find_one(activity_id)

        activity.add_evaluation(evaluation)

        await self.repository.update(activity)

        return ParticipantEvaluation(
            id=evaluation.id,
            participant_id=evaluation.participant_id,
        )
