from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Participant:
    """
    Representa um participante de uma atividade de avaliação.
    """
    name: str
    role: str
    id: UUID = field(default_factory=uuid4)
