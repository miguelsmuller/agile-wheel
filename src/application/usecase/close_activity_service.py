from src.application.ports.input.close_activity_port import CloseActivityPort
from src.domain.entities.activity import Activity


class CloseActivityService(CloseActivityPort):

    def __init__(self, repository = None):
        self.repository = repository

    async def execute(self, activity_id:str, participant_id_requested:str) -> Activity:
        activity = Activity(id=activity_id)

        def close_activity(activity_document):
            domain_activity = activity_document.to_domain()

            owner = next((p for p in domain_activity.participants if p.role == "owner"), None)
            if not owner or owner.id != participant_id_requested:
                raise PermissionError("Only the owner can close the activity")

            activity_document.opened = False

        return await self.repository.update(activity, close_activity)
