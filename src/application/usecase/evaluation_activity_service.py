from uuid import UUID

from src.application.ports.input.evaluation_activity_port import EvaluationActivityPort
from src.domain.entities.evaluation import ParticipantEvaluation


class EvaluationActivityService(EvaluationActivityPort):

    def __init__(self, repository = None):
        self.repository = repository

    def execute(
        self,
        activity_id: UUID,
        evaluation: ParticipantEvaluation
    ) -> ParticipantEvaluation:

        return ParticipantEvaluation(
            participant_id=evaluation.participant_id,
            id=evaluation.id
        )
