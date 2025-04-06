from abc import ABC, abstractmethod

from src.domain.models.activity import Activity
from src.domain.models.participant import Participant


class JoinActivityPort(ABC):
    @abstractmethod
    def execute(self, activity:Activity, participant: Participant) -> tuple[Activity, Participant]:
        pass
