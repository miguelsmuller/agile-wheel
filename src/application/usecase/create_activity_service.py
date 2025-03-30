from src.application.ports.input.http.create_activity_port import CreateActivityPort

from src.application.domain.models.activity import Activity


class CreateActivityService(CreateActivityPort):
    def execute(self):
        return Activity()
