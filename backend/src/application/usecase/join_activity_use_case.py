from uuid import UUID

from src.application.ports.input.join_activity_port import JoinActivityPort
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity
from src.domain.entities.participant import Participant
from src.domain.exceptions import ActivityNotFoundError


class JoinActivityService(JoinActivityPort):

    def __init__(self, repository: ActivityRepositoryPort = None):
        self.repository = repository

    async def execute(
        self,
        activity_id: UUID,
        participant: Participant
    ) -> tuple[Activity, Participant]:
        activity = await self.repository.find_one(activity_id)

        if activity is None:
            raise ActivityNotFoundError("Activity not found for join")

        activity.add_participant(participant)

        return await self.repository.update(activity), participant
