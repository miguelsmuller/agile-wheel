from uuid import UUID

from src.application.dto.activity_with_result import ActivityWithResult
from src.application.ports.input.get_activity_result_port import GetActivityResultPort
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.aggregations.activity_result import ActivityResult


class GetActivityResultService(GetActivityResultPort):

    def __init__(self, repository: ActivityRepositoryPort = None):
        self.repository  = repository

    async def get_activity_result(
        self, activity_id: UUID
    ) -> ActivityWithResult:
        activity = await self.repository.find_one(activity_id)

        if activity is None:
            raise ReferenceError("Activity not found for update")

        return ActivityWithResult(
            activity=activity,
            result=ActivityResult.from_activity(activity)
        )
