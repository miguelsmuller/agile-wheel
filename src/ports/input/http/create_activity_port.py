from abc import ABC, abstractmethod

class ActivityPort(ABC):
    @abstractmethod
    def create_activity(self):
        pass
