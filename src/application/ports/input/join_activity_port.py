from abc import ABC, abstractmethod

from src.domain.entities.activity import Activity
from src.domain.entities.participant import Participant


class JoinActivityPort(ABC):
    @abstractmethod
    def execute(self, activity:Activity, participant: Participant) -> tuple[Activity, Participant]:
        pass
