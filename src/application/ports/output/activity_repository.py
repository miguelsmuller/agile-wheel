from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.activity import Activity


class ActivityRepositoryPort(ABC):
    @abstractmethod
    async def create(self, user: Activity) -> Activity: ...

    @abstractmethod
    async def update(self, user: Activity) -> Activity: ...

    @abstractmethod
    async def find_one(self, activity_id: UUID) -> Activity | None: ...

    @abstractmethod
    async def find_all(self) -> list[Activity]: ...
