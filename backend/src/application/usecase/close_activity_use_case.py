from uuid import UUID

from src.application.ports.input.close_activity_port import CloseActivityPort
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity


class CloseActivityService(CloseActivityPort):

    def __init__(self, repository: ActivityRepositoryPort = None):
        self.repository = repository

    async def execute(self, activity_id:UUID, participant_id_requested:UUID) -> Activity:
        activity = await self.repository.find_one(activity_id)

        if not activity:
            raise ReferenceError("Activity not found for update")

        if not activity.owner or activity.owner.id != participant_id_requested:
            raise PermissionError("Only the owner can close the activity")

        activity.is_opened = False

        return await self.repository.update(activity)
