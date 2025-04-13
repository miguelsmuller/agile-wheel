from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.activity import Activity


class StatusActivityPort(ABC):
    @abstractmethod
    def execute(self, activity_id:UUID, participant_id: UUID) -> Activity:
        pass
