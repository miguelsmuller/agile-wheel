from abc import ABC, abstractmethod

from src.domain.models.activity import Activity
from src.domain.models.participant import Participant


class CreateActivityPort(ABC):
    @abstractmethod
    def execute(self, owner: Participant) -> Activity:
        pass
