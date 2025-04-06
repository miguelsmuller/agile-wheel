from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.domain.models.activity import Activity
from src.domain.models.dimension import Dimension
from src.domain.models.participant import Participant
from src.application.ports.input.create_activity_port import CreateActivityPort


class CreateActivityService(CreateActivityPort):

    def __init__(self, repository = None):
        self.repository = repository or ActivityRepositoryAdapter()

    @staticmethod
    def get_service() -> CreateActivityPort:
        return CreateActivityService()

    async def execute(self, owner: Participant) -> Activity:
        activity = Activity()

        activity.add_dimension(Dimension(id="experimente_e_aprenda", dimension="Experimente e Aprenda"))
        activity.add_dimension(Dimension(id="seguranca", dimension="Segurança"))
        activity.add_dimension(Dimension(id="valor_a_todo_instante", dimension="Valor a todo instante"))

        activity.add_participant(owner)

        return await self.repository.save(activity)
