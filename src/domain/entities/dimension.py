from dataclasses import dataclass


@dataclass
class Dimension:
    """Representa uma dimensão da agilidade a ser avaliada."""

    id: str  # Identificador slug único da dimensão
    dimension: str  # Nome da dimensão
    comments: str | None = None
