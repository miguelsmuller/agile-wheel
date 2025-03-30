from src.adapters.output.database.activity_repository_mongo import ActivityRepositoryMongo
from src.application.domain.models.dimension import Dimension
from src.application.ports.input.http.create_activity_port import CreateActivityPort

from src.application.domain.models.activity import Activity


class CreateActivityService(CreateActivityPort):

    def __init__(self, repo = None):
        self.repo = repo or ActivityRepositoryMongo()

    async def execute(self):
        activity = Activity()

        activity.add_dimension(Dimension(id="experimente_e_aprenda", dimension="Experimente e Aprenda"))
        activity.add_dimension(Dimension(id="seguranca", dimension="Segurança"))
        activity.add_dimension(Dimension(id="valor_a_todo_instante", dimension="Valor a todo instante"))

        activity: Activity = await self.repo.save(activity)

        return activity
