from abc import ABC, abstractmethod

class CreateActivityPort(ABC):
    @abstractmethod
    def execute(self):
        pass
