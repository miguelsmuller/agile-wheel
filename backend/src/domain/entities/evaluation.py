from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Rating:
    """Representa um voto individual de um participante para uma dimensão específica."""

    principle_id: str
    score: float
    comments: str | None = None


@dataclass
class ParticipantEvaluation:
    """Conjunto de votos fornecidos por um participante em uma atividade."""

    participant_id: UUID
    id: UUID = field(default_factory=uuid4)
    ratings: list[Rating] = field(default_factory=list)

    def add_vote(self, vote: Rating) -> None:
        self.ratings.append(vote)

    def has_voted_for(self, dimension_id: str) -> bool:
        return any(v.dimension_id == dimension_id for v in self.ratings)
