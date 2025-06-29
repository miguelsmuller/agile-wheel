from abc import ABC, abstractmethod
from uuid import UUID

from src.application.dto.activity_with_result import ActivityWithResult
from src.domain.entities.activity import Activity


class GetActivityPort(ABC):
    @abstractmethod
    def get_activity(self, activity_id:UUID, participant_id: UUID) -> Activity:
        pass  # pragma: no cover

    @abstractmethod
    def get_activity_with_result(self, activity_id: UUID) -> ActivityWithResult:
        pass  # pragma: no cover

