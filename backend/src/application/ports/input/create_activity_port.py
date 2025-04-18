from abc import ABC, abstractmethod

from src.domain.entities.activity import Activity
from src.domain.entities.participant import Participant


class CreateActivityPort(ABC):
    @abstractmethod
    def execute(self, owner: Participant) -> Activity:
        pass
