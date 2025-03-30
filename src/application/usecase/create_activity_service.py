from src.application.ports.input.http.create_activity_port import ActivityPort

from src.application.domain.models.activity import Activity


class ActivityService(ActivityPort):
    def create_activity(self):
        return Activity()
