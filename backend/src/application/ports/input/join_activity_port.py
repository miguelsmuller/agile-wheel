from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.activity import Activity
from src.domain.entities.participant import Participant


class JoinActivityPort(ABC):
    @abstractmethod
    def execute(self, activity_id:UUID, participant: Participant) -> tuple[Activity, Participant]:
        pass  # pragma: no cover
