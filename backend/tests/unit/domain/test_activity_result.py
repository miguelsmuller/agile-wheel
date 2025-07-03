from uuid import uuid4

import pytest

from src.domain.entities.activity import Activity
from src.domain.entities.dimension import Dimension, Principle
from src.domain.entities.evaluation import ParticipantEvaluation, Rating
from src.domain.entities.participant import Participant


def test_activity_result_by_principle():
    # Given
    activity = Activity()

    activity.add_dimension(
        Dimension(id="experimente", name="Experimente", principles=[
            Principle(id="compartilhamento", name="Compartilhamento"),
            Principle(id="comprometimento", name="Comprometimento")
        ])
    )
    activity.add_dimension(
        Dimension(id="seguranca", name="Segurança", principles=[
            Principle(id="sustentabilidade", name="Sustentabilidade"),
            Principle(id="metricas", name="Métricas Ágeis")
        ])
    )

    part1 = Participant(name="Ana", email="ana@ex.com", role="owner", id=uuid4())
    part2 = Participant(name="João", email="joao@ex.com", role="member", id=uuid4())

    activity.add_participant(part1)
    activity.add_participant(part2)

    ev1 = ParticipantEvaluation(participant_id=part1.id)
    ev1.add_vote(Rating(principle_id="compartilhamento", score=4))
    ev1.add_vote(Rating(principle_id="comprometimento", score=3))
    ev1.add_vote(Rating(principle_id="sustentabilidade", score=5))
    ev1.add_vote(Rating(principle_id="metricas", score=2))
    activity.add_evaluation(ev1)

    ev2 = ParticipantEvaluation(participant_id=part2.id)
    ev2.add_vote(Rating(principle_id="compartilhamento", score=2))
    ev2.add_vote(Rating(principle_id="comprometimento", score=5))
    ev2.add_vote(Rating(principle_id="sustentabilidade", score=4))
    ev2.add_vote(Rating(principle_id="metricas", score=3))
    activity.add_evaluation(ev2)

    # When
    result = activity.result

    # Then
    principle_scores = {
        pr.principle.id: pr.average_score
        for d in result.dimension_scores
        for pr in d.principles
    }

    # From Dimension 1
    assert principle_scores["compartilhamento"] == pytest.approx(3.0)    # (4+2)/2
    assert principle_scores["comprometimento"] == pytest.approx(4.0)     # (3+5)/2
    # From Dimension 2
    assert principle_scores["sustentabilidade"] == pytest.approx(4.5)    # (5+4)/2
    assert principle_scores["metricas"] == pytest.approx(2.5)            # (2+3)/2
