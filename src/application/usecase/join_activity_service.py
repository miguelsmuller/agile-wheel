from src.application.domain.models.activity import Activity
from src.application.domain.models.participant import Participant
from src.application.domain.models.dimension import Dimension
from src.application.ports.input.http.join_activity_port import JoinActivityPort


class JoinActivityService(JoinActivityPort):
    def execute(self, activity: Activity, participant: Participant):
        activity = Activity()

        activity.add_dimension(Dimension(id="experimente_e_aprenda", dimension="Experimente e Aprenda"))
        activity.add_dimension(Dimension(id="seguranca", dimension="Segurança"))
        activity.add_dimension(Dimension(id="valor_a_todo_instante", dimension="Valor a todo instante"))

        activity.add_participant(participant)

        return activity
