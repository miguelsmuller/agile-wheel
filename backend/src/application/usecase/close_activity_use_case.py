import logging
from uuid import UUID

from src.application.ports.input.close_activity_port import CloseActivityPort
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity
from src.domain.exceptions import ActivityNotFoundError, PermissionDeniedError

logger = logging.getLogger(__name__)

class CloseActivityService(CloseActivityPort):

    def __init__(self, repository: ActivityRepositoryPort = None):
        self.repository = repository

    async def execute(self, activity_id:UUID, participant_id:UUID) -> Activity:
        log_data = {
            "activity_id": activity_id, "participant_id": participant_id
        }

        logger.debug("[CLOSE_ACTIVITY_SERVICE] Doing Business Logic", extra=log_data)

        activity = await self.repository.find_one(activity_id)

        if not activity:
            raise ActivityNotFoundError("Activity not found for close")

        if not activity.owner or activity.owner.id != participant_id:
            raise PermissionDeniedError("Only the owner can close the activity")

        activity.is_opened = False

        log_data["activity"] = activity
        log_data["repository"] = str(self.repository)
        logger.debug("[CLOSE_ACTIVITY_SERVICE] Closing activity", extra=log_data)

        return await self.repository.update(activity)
