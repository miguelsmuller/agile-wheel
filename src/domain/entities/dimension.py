from dataclasses import dataclass, field


@dataclass
class Principle:
    """Representa um princípio pertencente a uma dimensão do Agile Wheel."""

    id: str  # Identificador slug único da dimensão
    name: str  # Nome do princípio
    comments: str | None = None


@dataclass
class Dimension:
    """Representa uma dimensão da agilidade a ser avaliada."""

    id: str  # Identificador slug único da dimensão
    name: str  # Nome da dimensão
    comments: str | None = None
    principles: list[Principle] = field(default_factory=list)
