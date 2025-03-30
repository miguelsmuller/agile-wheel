from src.application.domain.models.dimension import Dimension
from src.application.ports.input.http.create_activity_port import CreateActivityPort

from src.application.domain.models.activity import Activity


class CreateActivityService(CreateActivityPort):
    def execute(self):
        activity = Activity()

        activity.add_dimension(Dimension(id="experimente_e_aprenda", dimension="Experimente e Aprenda"))
        activity.add_dimension(Dimension(id="seguranca", dimension="Segurança"))
        activity.add_dimension(Dimension(id="valor_a_todo_instante", dimension="Valor a todo instante"))

        return activity
