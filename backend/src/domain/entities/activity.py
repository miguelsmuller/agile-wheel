from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.aggregations.activity_result import ActivityResult

from .dimension import Dimension
from .evaluation import ParticipantEvaluation
from .participant import Participant


@dataclass
class Activity:
    """Representa uma sessão de avaliação ágil, incluindo os participantes,
    as dimensões avaliadas e as avaliações feitas.
    """

    id: UUID = field(default_factory=uuid4)
    is_opened: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    participants: list[Participant] = field(default_factory=list)
    dimensions: list[Dimension] = field(default_factory=list)
    evaluations: list[ParticipantEvaluation] = field(default_factory=list)

    @property
    def owner(self) -> Participant | None:
        return next((p for p in self.participants if p.role == "owner"), None)

    @property
    def result(self) -> "ActivityResult":
        return ActivityResult.from_activity(self)

    def add_participant(self, participant: Participant) -> None:
        if participant not in self.participants:
            self.participants.append(participant)

    def add_dimension(self, dimension: Dimension) -> None:
        if dimension.id not in [d.id for d in self.dimensions]:
            self.dimensions.append(dimension)

    def add_evaluation(self, evaluation: ParticipantEvaluation) -> None:
        self.evaluations.append(evaluation)
