from src.ports.input.http.create_activity_port import ActivityPort

from src.domain.models.activity import Activity


class ActivityService(ActivityPort):
    def create_activity(self):
        return Activity()
