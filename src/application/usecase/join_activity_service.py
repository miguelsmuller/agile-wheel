from src.adapters.output.schema.activity_document_mongo import ActivityDocument
from src.application.domain.models.activity import Activity
from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.application.domain.models.participant import Participant
from src.application.ports.input.join_activity_port import JoinActivityPort


class JoinActivityService(JoinActivityPort):

    def __init__(self, repository = None):
        self.repository = repository or ActivityRepositoryAdapter()

    @staticmethod
    def get_service() -> JoinActivityPort:
        return JoinActivityService()
    
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
