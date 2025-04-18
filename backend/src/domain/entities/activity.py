from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from .dimension import Dimension
from .evaluation import ParticipantEvaluation
from .participant import Participant


@dataclass
class DimensionResult:
    dimension: Dimension
    average_score: float
    total_ratings: int


@dataclass
class ActivityResult:
    """ActivityResult é um dado derivado — ele não representa algo que precisa ser
    armazenado dentro de Activity, mas sim algo que é calculado a partir de seu estado atual.
    """

    overall_score: float = 0.0
    dimension_scores: list[DimensionResult] = field(default_factory=list)

    @classmethod
    def from_activity(cls, activity: "Activity") -> "ActivityResult":
        dimension_map = {d.id: d for d in activity.dimensions}
        scores = {d.id: [] for d in activity.dimensions}

        for evaluation in activity.evaluations:
            for vote in evaluation.ratings:
                if vote.dimension_id in scores:
                    scores[vote.dimension_id].append(vote.score)

        dimension_scores = []
        total_score = 0
        for dim_id, votes in scores.items():
            if votes:
                avg = sum(votes) / len(votes)
                total_score += avg
                dimension_scores.append(
                    DimensionResult(
                        dimension=dimension_map[dim_id],
                        average_score=avg,
                        total_ratings=len(votes),
                    )
                )

        overall_score = total_score / len(dimension_scores) if dimension_scores else 0
        return cls(overall_score=overall_score, dimension_scores=dimension_scores)


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

    def generate_result(self) -> ActivityResult:
        return ActivityResult.from_activity(self)

    def add_participant(self, participant: Participant) -> None:
        if participant not in self.participants:
            self.participants.append(participant)

    def add_dimension(self, dimension: Dimension) -> None:
        if dimension.id not in [d.id for d in self.dimensions]:
            self.dimensions.append(dimension)

    def add_evaluation(self, evaluation: ParticipantEvaluation) -> None:
        self.evaluations.append(evaluation)
