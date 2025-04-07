from src.application.ports.input.create_activity_port import CreateActivityPort
from src.domain.entities.activity import Activity
from src.domain.entities.dimension import Dimension
from src.domain.entities.participant import Participant


class CreateActivityService(CreateActivityPort):
    def __init__(self, repository=None):
        self.repository = repository

    async def execute(self, owner: Participant) -> Activity:
        activity = Activity()

        activity.opened = True
        activity.add_dimension(
            Dimension(id="experimente_e_aprenda", dimension="Experimente e Aprenda")
        )
        activity.add_dimension(Dimension(id="seguranca", dimension="Segurança"))
        activity.add_dimension(
            Dimension(id="valor_a_todo_instante", dimension="Valor a todo instante")
        )

        activity.add_participant(owner)

        return await self.repository.create(activity)
