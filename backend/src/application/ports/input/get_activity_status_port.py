from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.activity import Activity


class GetActivityStatusPort(ABC):
    @abstractmethod
    def get_activity_status(self, activity_id:UUID, participant_id: UUID) -> Activity:
        pass  # pragma: no cover
