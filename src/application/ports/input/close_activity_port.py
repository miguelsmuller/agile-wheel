from abc import ABC, abstractmethod

from src.application.domain.models.activity import Activity


class CloseActivityPort(ABC):
    @abstractmethod
    def execute(self, activity_id:str, participant_id_requested:str) -> Activity:
        pass
