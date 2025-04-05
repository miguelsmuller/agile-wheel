from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.application.domain.models.dimension import Dimension
from src.application.domain.models.participant import Participant
from src.application.ports.input.create_activity_port import CreateActivityPort
from src.application.domain.models.activity import Activity


class CreateActivityService(CreateActivityPort):

    def __init__(self, repo = None):
        self.repo = repo or ActivityRepositoryAdapter()

    @staticmethod
    def get_service() -> CreateActivityPort:
        return CreateActivityService()

    async def execute(self, owner: Participant) -> Activity:
        activity = Activity()

        activity.add_dimension(Dimension(id="experimente_e_aprenda", dimension="Experimente e Aprenda"))
        activity.add_dimension(Dimension(id="seguranca", dimension="Segurança"))
        activity.add_dimension(Dimension(id="valor_a_todo_instante", dimension="Valor a todo instante"))
        
        activity.add_participant(owner)

        activity: Activity = await self.repo.save(activity)

        return activity
