from abc import ABC, abstractmethod

from src.application.domain.models.activity import Activity
from src.application.domain.models.participant import Participant

class JoinActivityPort(ABC):
    @abstractmethod
    def execute(self, activity:Activity, participant: Participant):
        pass
