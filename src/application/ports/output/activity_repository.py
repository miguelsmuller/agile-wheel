# src/ports/output/user_repository.py
from abc import ABC, abstractmethod
from src.application.domain.models.activity import Activity
from typing import List

class ActivityRepositoryPort(ABC):
    @abstractmethod
    async def save(self, user: Activity) -> Activity: ...

    @abstractmethod
    async def update(self, user: Activity) -> Activity: ...
    
    @abstractmethod
    async def find_all(self) -> List[Activity]: ...
