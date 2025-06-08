from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.domain.entities.dimension import Dimension, Principle

if TYPE_CHECKING:
    from src.domain.entities.activity import Activity


@dataclass
class PrincipleResult:
    principle: Principle
    average_score: float
    total_ratings: int

@dataclass
class DimensionResult:
    dimension: Dimension
    average_score: float
    total_ratings: int
    principles: list[PrincipleResult] = field(default_factory=list)


@dataclass
class ActivityResult:
    """Represents an aggregated summary of an Agile Wheel activity.

    This data class is a *read model* calculated from the current state of an `Activity`.
    It provides derived information such as:
      - The average score for each principle (across all participants)
      - The average score for each dimension (based on its principles)
      - The overall activity score (global average)

    `ActivityResult` is not persisted in the database. Instead, it is generated on demand
    to provide a snapshot of the team's evaluation results, supporting features such as:
      - Result visualization (e.g., radar charts)
      - Reporting and exporting (PDF, dashboards)
      - API responses

    Attributes:
        overall_score (float): The global average score of the activity.
        dimension_scores (list[DimensionResult]): Aggregated results for each dimension,
            including their principles' averages and total votes.

    """

    overall_score: float = 0.0
    dimension_scores: list[DimensionResult] = field(default_factory=list)

    @classmethod
    def from_activity(cls, activity: "Activity") -> "ActivityResult":
        # Map all principles to their vote lists
        votes_by_principle = {}
        for dim in activity.dimensions:
            for principle in dim.principles:
                votes_by_principle[principle.id] = []

        # Aggregate all votes for each principle across all participant evaluations
        for evaluation in activity.evaluations:
            for vote in evaluation.ratings:
                if vote.principle_id in votes_by_principle:
                    votes_by_principle[vote.principle_id].append(vote.score)

        dimension_results = []
        all_scores = []

        # Calculate average and total votes for each principle and dimension
        for dim in activity.dimensions:
            principle_results = []
            for principle in dim.principles:
                scores = votes_by_principle[principle.id]
                avg = sum(scores) / len(scores) if scores else 0.0
                principle_results.append(
                    PrincipleResult(
                        principle=principle,
                        average_score=avg,
                        total_ratings=len(scores)
                    )
                )
                all_scores.extend(scores)
            # Dimension average is the average of its principles' averages
            avg_dim = (
                sum(pr.average_score for pr in principle_results) / len(principle_results)
                if principle_results else 0.0
            )
            total_ratings = sum(pr.total_ratings for pr in principle_results)
            dimension_results.append(
                DimensionResult(
                    dimension=dim,
                    principles=principle_results,
                    average_score=avg_dim,
                    total_ratings=total_ratings
                )
            )

        # Global average is the average of all submitted scores
        overall_score = (sum(all_scores) / len(all_scores)) if all_scores else 0.0

        return cls(overall_score=overall_score, dimension_scores=dimension_results)


