from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.evaluation import ParticipantEvaluation


class EvaluationActivityPort(ABC):
    @abstractmethod
    def execute(
        self,
        activity_id:UUID,
        evaluation:ParticipantEvaluation
    ) -> ParticipantEvaluation:
        pass  # pragma: no cover
