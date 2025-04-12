from uuid import UUID

from src.application.ports.input.close_activity_port import CloseActivityPort
from src.domain.entities.activity import Activity


class CloseActivityService(CloseActivityPort):

    def __init__(self, repository = None):
        self.repository = repository

    async def execute(self, activity_id:UUID, participant_id_requested:str) -> Activity:

        activity = await self.repository.find_one(activity_id)

        owner = next((p for p in activity.participants if p.role == "owner"), None)

        if not owner or owner.id != participant_id_requested:
            raise PermissionError("Only the owner can close the activity")

        activity.opened = False

        return await self.repository.update(activity)
