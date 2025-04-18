from typing import TYPE_CHECKING
from uuid import UUID

from src.application.ports.input.status_activity_port import StatusActivityPort
from src.domain.entities.activity import Activity

if TYPE_CHECKING:  # pragma: no cover
    from src.application.ports.output.activity_repository import ActivityRepositoryPort


class StatusActivityService(StatusActivityPort):

    def __init__(self, repository = None):
        self.repository: ActivityRepositoryPort = repository

    async def execute(
        self,
        activity_id: UUID,
        participant_id: UUID,
    ) -> Activity:
        activity = await self.repository.find_one(str(activity_id))

        if activity is None:
            raise ReferenceError("Activity not found for update")

        participant_ids = {p.id for p in activity.participants}
        if participant_id not in participant_ids:
            raise PermissionError("Only the members cant get the status")

        return activity
