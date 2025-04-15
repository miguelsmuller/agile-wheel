from datetime import datetime
from uuid import UUID

import pytest
import pytz
from beanie import init_beanie
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient
from src.adapters.output.activity_document_mongo import (
    ActivityDocument,
    DimensionModel,
    ParticipantEvaluationModel,
    ParticipantModel,
    PrincipleModel,
    RatingModel,
)
from src.domain.entities.activity import Activity
from src.domain.entities.dimension import Dimension, Principle
from src.domain.entities.evaluation import ParticipantEvaluation, Rating
from src.domain.entities.participant import Participant

# ****************************************************************
# * Mocking the database connection
# ****************************************************************

@pytest.fixture(autouse=True)
async def mock_init_beanie():
    client = AsyncMongoMockClient()

    await init_beanie(
        client.get_database(name="db"),
        document_models=[ActivityDocument]
    )

    yield client

# ****************************************************************
# * Mocking the Activity entity
# ****************************************************************

mock_uuid = "b3d59547-35fc-446d-b567-8ba6ab65f764"
mock_activity_uuid = UUID(mock_uuid)
mock_activity_created = datetime(
    2025, 4, 13, 10, 30, 00, 00, tzinfo=pytz.timezone("America/Sao_Paulo")
)

@pytest.fixture
def mock_activity_fixture():
    return Activity(
        id=mock_activity_uuid,
        is_opened=False,
        created_at=mock_activity_created,
        participants=[
            Participant(
                name="string",
                email="user@example.com",
                role="owner",
                id=UUID("b3d59547-35fc-446d-b567-8ba6ab65f764")
            ),
            Participant(
                name="string",
                email="user@example.com",
                role="regular",
                id=UUID("12d2beee-d4e3-4633-adce-248e5d9a6227")
            )
        ],
        dimensions=[
            Dimension(
                id="experimente",
                dimension="Experimente e Aprenda Rápido",
                comments=None,
                principles=[
                    Principle(
                        id="compartilhamento_de_conhecimento",
                        principle="Compartilhamento de conhecimento",
                        comments=None
                    ),
                    Principle(
                        id="comprometimento_com_o_produto",
                        principle="Comprometimento com o produto",
                        comments=None
                    ),
                    Principle(
                        id="praticas_lean_agile",
                        principle="Práticas Lean-Agile",
                        comments=None
                    ),
                    Principle(
                        id="ritmo_das_entregas",
                        principle="Ritmo das entregas",
                        comments=None
                    ),
                    Principle(
                        id="granularidade_de_demandas",
                        principle="Granularidade de demandas",
                        comments=None
                    )
                ]
            ),
            Dimension(
                id="pessoas",
                dimension="Pessoas Sensacionais",
                comments=None,
                principles=[
                    Principle(
                        id="colaboracao_e_comunicacao",
                        principle="Colaboração e comunicação",
                        comments=None
                    ),
                    Principle(
                        id="motivacao_e_confianca",
                        principle="Motivação e confiança",
                        comments=None
                    ),
                    Principle(
                        id="autonomia_e_auto_organizacao",
                        principle="Autonomia e auto-organização",
                        comments=None
                    ),
                    Principle(
                        id="melhoria_continua",
                        principle="Melhoria Contínua",
                        comments=None
                    ),
                    Principle(
                        id="interdisciplinaridade",
                        principle="Interdisciplinaridade",
                        comments=None
                    )
                ]
            ),
            Dimension(
                id="valor",
                dimension="Valor a Todo Instante",
                comments=None,
                principles=[
                    Principle(
                        id="discovery_upstream_kanban",
                        principle="Discovery/Upstream Kanban",
                        comments=None
                    ),
                    Principle(
                        id="user_experience_ux_ui",
                        principle="User Experience (UX/UI)",
                        comments=None
                    ),
                    Principle(
                        id="entrega_de_valor_percebido",
                        principle="Entrega de valor (percebido)",
                        comments=None
                    ),
                    Principle(
                        id="relacionamento_com_o_negocio",
                        principle="Relacionamento com o negócio",
                        comments=None
                    ),
                    Principle(
                        id="satisfacao_do_cliente",
                        principle="Satisfação do cliente",
                        comments=None
                    )
                ]
            ),
            Dimension(
                id="seguranca",
                dimension="Segurança é um Pré-requisito",
                comments=None,
                principles=[
                    Principle(
                        id="trabalho_sustentavel",
                        principle="Trabalho sustentável",
                        comments=None
                    ),
                    Principle(
                        id="metricas_ageis",
                        principle="Métricas Ágeis",
                        comments=None
                    ),
                    Principle(
                        id="estimativas_e_contratos_ageis",
                        principle="Estimativas & contratos ágeis",
                        comments=None
                    ),
                    Principle(
                        id="metas_orks",
                        principle="Metas/ORKs",
                        comments=None
                    ),
                    Principle(
                        id="desdobramentos_estrategicos",
                        principle="Desdobramentos estratégicos",
                        comments=None
                    )
                ]
            )
        ],
        evaluations=[
            ParticipantEvaluation(
                participant_id=UUID("12d2beee-d4e3-4633-adce-248e5d9a6227"),
                id=UUID("fc4097f9-9be6-4060-8281-56097fac8e37"),
                ratings=[
                    Rating(principle_id="string", score=0.0, comments="string")
                ]
            )
        ]
    )


@pytest.fixture
def mock_activity_document_fixture():
    return ActivityDocument(
        _id=ObjectId("67fa905024b5c557a228c505"),
        app_id=mock_uuid,
        is_opened=True,
        created_at=mock_activity_created,
        participants=[
            ParticipantModel(
                id="7870b158-4900-466a-948c-14b462b62f5b",
                name="Fulano de Tal",
                role="owner",
                email="fulano@example.com"
            ),
            ParticipantModel(
                id="3259afaa-29af-43ca-bcdd-3c52dfbfe2e7",
                name="Ciclano de Tal",
                role="regular",
                email="ciclano@example.com"
            )
        ],
        dimensions=[
            DimensionModel(
                id="experimente",
                dimension="Experimente e Aprenda Rápido",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="compartilhamento_de_conhecimento",
                        principle="Compartilhamento de conhecimento",
                        comments=None
                    ),
                    PrincipleModel(
                        id="comprometimento_com_o_produto",
                        principle="Comprometimento com o produto",
                        comments=None
                    ),
                    PrincipleModel(
                        id="praticas_lean_agile",
                        principle="Práticas Lean-Agile",
                        comments=None
                    ),
                    PrincipleModel(
                        id="ritmo_das_entregas",
                        principle="Ritmo das entregas",
                        comments=None
                    ),
                    PrincipleModel(
                        id="granularidade_de_demandas",
                        principle="Granularidade de demandas",
                        comments=None
                    )
                ]
            ),
            DimensionModel(
                id="pessoas",
                dimension="Pessoas Sensacionais",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="colaboracao_e_comunicacao",
                        principle="Colaboração e comunicação",
                        comments=None
                    ),
                    PrincipleModel(
                        id="motivacao_e_confianca",
                        principle="Motivação e confiança",
                        comments=None
                    ),
                    PrincipleModel(
                        id="autonomia_e_auto_organizacao",
                        principle="Autonomia e auto-organização",
                        comments=None
                    ),
                    PrincipleModel(
                        id="melhoria_continua",
                        principle="Melhoria Contínua",
                        comments=None
                    ),
                    PrincipleModel(
                        id="interdisciplinaridade",
                        principle="Interdisciplinaridade",
                        comments=None
                    )
                ]
            ),
            DimensionModel(
                id="valor",
                dimension="Valor a Todo Instante",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="discovery_upstream_kanban",
                        principle="Discovery/Upstream Kanban",
                        comments=None
                    ),
                    PrincipleModel(
                        id="user_experience_ux_ui",
                        principle="User Experience (UX/UI)",
                        comments=None
                    ),
                    PrincipleModel(
                        id="entrega_de_valor_percebido",
                        principle="Entrega de valor (percebido)",
                        comments=None
                    ),
                    PrincipleModel(
                        id="relacionamento_com_o_negocio",
                        principle="Relacionamento com o negócio",
                        comments=None
                    ),
                    PrincipleModel(
                        id="satisfacao_do_cliente",
                        principle="Satisfação do cliente",
                        comments=None
                    )
                ]
            ),
            DimensionModel(
                id="seguranca",
                dimension="Segurança é um Pré-requisito",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="trabalho_sustentavel",
                        principle="Trabalho sustentável",
                        comments=None
                    ),
                    PrincipleModel(
                        id="metricas_ageis",
                        principle="Métricas Ágeis",
                        comments=None
                    ),
                    PrincipleModel(
                        id="estimativas_e_contratos_ageis",
                        principle="Estimativas & contratos ágeis",
                        comments=None
                    ),
                    PrincipleModel(
                        id="metas_orks",
                        principle="Metas/ORKs",
                        comments=None
                    ),
                    PrincipleModel(
                        id="desdobramentos_estrategicos",
                        principle="Desdobramentos estratégicos",
                        comments=None
                    )
                ]
            )
        ],
        evaluations=[
            ParticipantEvaluationModel(
                id="2de19d29-1692-4540-8e91-e278a8148b6b",
                participant_id="7870b158-4900-466a-948c-14b462b62f5b",
                ratings=[
                    RatingModel(
                        principle_id="compartilhamento_de_conhecimento",
                        score=5.7,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="comprometimento_com_o_produto",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="praticas_lean_agile",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="ritmo_das_entregas",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="granularidade_de_demandas",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="colaboracao_e_comunicacao",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="motivacao_e_confianca",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="autonomia_e_auto_organizacao",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="melhoria_continua",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="interdisciplinaridade",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="discovery_upstream_kanban",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="user_experience_ux_ui",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="entrega_de_valor_percebido",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="relacionamento_com_o_negocio",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="satisfacao_do_cliente",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="trabalho_sustentavel",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="metricas_ageis",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="estimativas_e_contratos_ageis",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="metas_orks",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="desdobramentos_estrategicos",
                        score=1.3,
                        comments=None
                    )
                ]
            ),
            ParticipantEvaluationModel(
                id="828cd348-385c-4e54-b743-68700eed0182",
                participant_id="3259afaa-29af-43ca-bcdd-3c52dfbfe2e7",
                ratings=[
                    RatingModel(
                        principle_id="compartilhamento_de_conhecimento",
                        score=5.7,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="comprometimento_com_o_produto",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="praticas_lean_agile",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="ritmo_das_entregas",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="granularidade_de_demandas",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="colaboracao_e_comunicacao",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="motivacao_e_confianca",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="autonomia_e_auto_organizacao",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="melhoria_continua",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="interdisciplinaridade",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="discovery_upstream_kanban",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="user_experience_ux_ui",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="entrega_de_valor_percebido",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="relacionamento_com_o_negocio",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="satisfacao_do_cliente",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="trabalho_sustentavel",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="metricas_ageis",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="estimativas_e_contratos_ageis",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="metas_orks",
                        score=1.3,
                        comments=None
                    ),
                    RatingModel(
                        principle_id="desdobramentos_estrategicos",
                        score=1.3,
                        comments=None
                    )
                ]
            )
        ]
    )
