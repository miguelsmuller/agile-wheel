from abc import ABC, abstractmethod
from uuid import UUID

from src.application.dto.activity_with_result import ActivityWithResult


class GetActivityResultPort(ABC):
    @abstractmethod
    def get_activity_result(self, activity_id: UUID) -> ActivityWithResult:
        pass  # pragma: no cover

