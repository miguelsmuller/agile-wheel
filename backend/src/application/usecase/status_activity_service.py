from uuid import UUID

from src.application.ports.input.status_activity_port import StatusActivityPort
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity


class StatusActivityService(StatusActivityPort):

    def __init__(self, repository: ActivityRepositoryPort = None):
        self.repository  = repository

    async def execute(
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
