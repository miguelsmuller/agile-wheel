from src.adapters.output.activity_document_mongo import ActivityDocument
from src.application.ports.input.join_activity_port import JoinActivityPort
from src.domain.entities.activity import Activity
from src.domain.entities.participant import Participant


class JoinActivityService(JoinActivityPort):

    def __init__(self, repository = None):
        self.repository = repository

    async def execute(
        self,
        activity: Activity,
        participant: Participant
    ) -> tuple[Activity, Participant]:

        def add_participant_callback(activity_document):
            domain_activity = activity_document.to_domain()
            domain_activity.add_participant(participant)
            updated_document = ActivityDocument.from_domain(domain_activity)
            activity_document.participants = updated_document.participants

        return await self.repository.update(activity, add_participant_callback), participant
