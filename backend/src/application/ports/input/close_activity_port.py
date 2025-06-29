from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.activity import Activity


class CloseActivityPort(ABC):
    @abstractmethod
    def execute(self, activity_id:UUID, participant_id_requested:str) -> Activity:
        pass  # pragma: no cover
