from src.application.domain.models.dimension import Dimension
from src.application.ports.input.http.create_activity_port import CreateActivityPort

from src.application.domain.models.activity import Activity


class CreateActivityService(CreateActivityPort):
    def execute(self):
        return Activity(
            dimensions=[
                Dimension(id="experimente_e_aprenda", dimension="Experimente e Aprenda"),
                Dimension(id="seguranca", dimension="Segurança"),
                Dimension(id="valor_a_todo_instante", dimension="Valor a todo instante"),
            ]
        )
