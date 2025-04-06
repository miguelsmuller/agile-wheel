from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .participant import Participant


@dataclass
class Rating:
    """Representa um voto individual de um participante para uma dimensão específica.
    """

    dimension_id: str
    score: float
    comments: str | None = None


@dataclass
class ParticipantEvaluation:
    """Conjunto de votos fornecidos por um participante em uma atividade.
    """

    participant: Participant
    id: UUID = field(default_factory=uuid4)
    ratings: list[Rating] = field(default_factory=list)

    def add_vote(self, vote: Rating) -> None:
        self.ratings.append(vote)

    def has_voted_for(self, dimension_id: str) -> bool:
        return any(v.dimension_id == dimension_id for v in self.ratings)
