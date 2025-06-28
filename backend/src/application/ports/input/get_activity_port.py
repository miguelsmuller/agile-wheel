from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.activity import Activity


class GetActivityPort(ABC):
    @abstractmethod
    def get_activity(self, activity_id:UUID, participant_id: UUID) -> Activity:
        pass
