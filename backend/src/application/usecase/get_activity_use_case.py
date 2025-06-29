from uuid import UUID

from src.application.dto.activity_with_result import ActivityWithResult
from src.application.ports.input.get_activity_port import GetActivityPort
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.aggregations.activity_result import ActivityResult
from src.domain.entities.activity import Activity


class GetActivityService(GetActivityPort):

    def __init__(self, repository: ActivityRepositoryPort = None):
        self.repository  = repository

    async def get_activity(
        self,
        activity_id: UUID,
        participant_id: UUID,
    ) -> Activity:
        activity = await self.repository.find_one(activity_id)

        if activity is None:
            raise ReferenceError("Activity not found for update")

        participant_ids = {p.id for p in activity.participants}
        if participant_id not in participant_ids:
            raise PermissionError("Only the members cant get the status")

        return activity

    async def get_activity_with_result(
        self, activity_id: UUID
    ) -> ActivityWithResult:
        activity = await self.repository.find_one(activity_id)

        if activity is None:
            raise ReferenceError("Activity not found for update")

        return ActivityWithResult(
            activity=activity,
            result=ActivityResult.from_activity(activity)
        )
