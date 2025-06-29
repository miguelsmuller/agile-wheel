from dataclasses import dataclass

from src.domain.aggregations.activity_result import ActivityResult
from src.domain.entities.activity import Activity


@dataclass(frozen=True)
class ActivityWithResult:
    activity: Activity
    result: ActivityResult
