from datetime import datetime
from uuid import UUID

import pytest
import pytz
from beanie import init_beanie
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient
from src.adapters.persistence.activity_document import (
    ActivityDocumentForMongo,
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
        document_models=[ActivityDocumentForMongo]
    )

    yield client

# ****************************************************************
# * Mocking the Activity entity
# ****************************************************************

mock_activity_created = datetime(
    2025, 4, 13, 10, 30, 00, 00, tzinfo=pytz.timezone("America/Sao_Paulo")
)

@pytest.fixture
def mock_uuid_string():
    return "b3d59547-35fc-446d-b567-8ba6ab65f764"


@pytest.fixture
def mock_uuid(mock_uuid_string):
    return UUID(mock_uuid_string)


@pytest.fixture
def mock_participant_owner():
    return Participant(
        name="string",
        email="user@example.com",
        role="owner",
        id=UUID("7870b158-4900-466a-948c-14b462b62f5b")
    )


@pytest.fixture
def mock_participant_model_owner(mock_participant_owner):
    return ParticipantModel(
        name=mock_participant_owner.name,
        email=mock_participant_owner.email,
        role=mock_participant_owner.role,
        id=str(mock_participant_owner.id)
    )


@pytest.fixture
def mock_participant_regular():
    return Participant(
        name="string",
        email="user@example.com",
        role="regular",
        id=UUID("3259afaa-29af-43ca-bcdd-3c52dfbfe2e7")
    )


@pytest.fixture
def mock_participant_model_regular(mock_participant_regular):
    return ParticipantModel(
        name=mock_participant_regular.name,
        email=mock_participant_regular.email,
        role=mock_participant_regular.role,
        id=str(mock_participant_regular.id)
    )


@pytest.fixture
def mock_activity_fixture(
    mock_uuid, mock_participant_owner, mock_participant_regular
):
    return Activity(
        id=mock_uuid,
        is_opened=False,
        created_at=mock_activity_created,
        participants=[
            mock_participant_owner,
            mock_participant_regular
        ],
        dimensions=[
            Dimension(
                id="experimente",
                name="Experimente e Aprenda Rápido",
                comments=None,
                principles=[
                    Principle(
                        id="compartilhamento_de_conhecimento",
                        name="Compartilhamento de conhecimento",
                        comments=None
                    ),
                    Principle(
                        id="comprometimento_com_o_produto",
                        name="Comprometimento com o produto",
                        comments=None
                    ),
                    Principle(
                        id="praticas_lean_agile",
                        name="Práticas Lean-Agile",
                        comments=None
                    ),
                    Principle(
                        id="ritmo_das_entregas",
                        name="Ritmo das entregas",
                        comments=None
                    ),
                    Principle(
                        id="granularidade_de_demandas",
                        name="Granularidade de demandas",
                        comments=None
                    )
                ]
            ),
            Dimension(
                id="pessoas",
                name="Pessoas Sensacionais",
                comments=None,
                principles=[
                    Principle(
                        id="colaboracao_e_comunicacao",
                        name="Colaboração e comunicação",
                        comments=None
                    ),
                    Principle(
                        id="motivacao_e_confianca",
                        name="Motivação e confiança",
                        comments=None
                    ),
                    Principle(
                        id="autonomia_e_auto_organizacao",
                        name="Autonomia e auto-organização",
                        comments=None
                    ),
                    Principle(
                        id="melhoria_continua",
                        name="Melhoria Contínua",
                        comments=None
                    ),
                    Principle(
                        id="interdisciplinaridade",
                        name="Interdisciplinaridade",
                        comments=None
                    )
                ]
            ),
            Dimension(
                id="valor",
                name="Valor a Todo Instante",
                comments=None,
                principles=[
                    Principle(
                        id="discovery_upstream_kanban",
                        name="Discovery/Upstream Kanban",
                        comments=None
                    ),
                    Principle(
                        id="user_experience_ux_ui",
                        name="User Experience (UX/UI)",
                        comments=None
                    ),
                    Principle(
                        id="entrega_de_valor_percebido",
                        name="Entrega de valor (percebido)",
                        comments=None
                    ),
                    Principle(
                        id="relacionamento_com_o_negocio",
                        name="Relacionamento com o negócio",
                        comments=None
                    ),
                    Principle(
                        id="satisfacao_do_cliente",
                        name="Satisfação do cliente",
                        comments=None
                    )
                ]
            ),
            Dimension(
                id="seguranca",
                name="Segurança é um Pré-requisito",
                comments=None,
                principles=[
                    Principle(
                        id="trabalho_sustentavel",
                        name="Trabalho sustentável",
                        comments=None
                    ),
                    Principle(
                        id="metricas_ageis",
                        name="Métricas Ágeis",
                        comments=None
                    ),
                    Principle(
                        id="estimativas_e_contratos_ageis",
                        name="Estimativas & contratos ágeis",
                        comments=None
                    ),
                    Principle(
                        id="metas_orks",
                        name="Metas/ORKs",
                        comments=None
                    ),
                    Principle(
                        id="desdobramentos_estrategicos",
                        name="Desdobramentos estratégicos",
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
def mock_activity_document_fixture(
    mock_uuid_string, mock_participant_model_owner, mock_participant_model_regular
):
    return ActivityDocumentForMongo(
        _id=ObjectId("67fa905024b5c557a228c505"),
        app_id=mock_uuid_string,
        is_opened=True,
        created_at=mock_activity_created,
        participants=[
            mock_participant_model_owner,
            mock_participant_model_regular
        ],
        dimensions=[
            DimensionModel(
                id="experimente",
                name="Experimente e Aprenda Rápido",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="compartilhamento_de_conhecimento",
                        name="Compartilhamento de conhecimento",
                        comments=None
                    ),
                    PrincipleModel(
                        id="comprometimento_com_o_produto",
                        name="Comprometimento com o produto",
                        comments=None
                    ),
                    PrincipleModel(
                        id="praticas_lean_agile",
                        name="Práticas Lean-Agile",
                        comments=None
                    ),
                    PrincipleModel(
                        id="ritmo_das_entregas",
                        name="Ritmo das entregas",
                        comments=None
                    ),
                    PrincipleModel(
                        id="granularidade_de_demandas",
                        name="Granularidade de demandas",
                        comments=None
                    )
                ]
            ),
            DimensionModel(
                id="pessoas",
                name="Pessoas Sensacionais",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="colaboracao_e_comunicacao",
                        name="Colaboração e comunicação",
                        comments=None
                    ),
                    PrincipleModel(
                        id="motivacao_e_confianca",
                        name="Motivação e confiança",
                        comments=None
                    ),
                    PrincipleModel(
                        id="autonomia_e_auto_organizacao",
                        name="Autonomia e auto-organização",
                        comments=None
                    ),
                    PrincipleModel(
                        id="melhoria_continua",
                        name="Melhoria Contínua",
                        comments=None
                    ),
                    PrincipleModel(
                        id="interdisciplinaridade",
                        name="Interdisciplinaridade",
                        comments=None
                    )
                ]
            ),
            DimensionModel(
                id="valor",
                name="Valor a Todo Instante",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="discovery_upstream_kanban",
                        name="Discovery/Upstream Kanban",
                        comments=None
                    ),
                    PrincipleModel(
                        id="user_experience_ux_ui",
                        name="User Experience (UX/UI)",
                        comments=None
                    ),
                    PrincipleModel(
                        id="entrega_de_valor_percebido",
                        name="Entrega de valor (percebido)",
                        comments=None
                    ),
                    PrincipleModel(
                        id="relacionamento_com_o_negocio",
                        name="Relacionamento com o negócio",
                        comments=None
                    ),
                    PrincipleModel(
                        id="satisfacao_do_cliente",
                        name="Satisfação do cliente",
                        comments=None
                    )
                ]
            ),
            DimensionModel(
                id="seguranca",
                name="Segurança é um Pré-requisito",
                comments=None,
                principles=[
                    PrincipleModel(
                        id="trabalho_sustentavel",
                        name="Trabalho sustentável",
                        comments=None
                    ),
                    PrincipleModel(
                        id="metricas_ageis",
                        name="Métricas Ágeis",
                        comments=None
                    ),
                    PrincipleModel(
                        id="estimativas_e_contratos_ageis",
                        name="Estimativas & contratos ágeis",
                        comments=None
                    ),
                    PrincipleModel(
                        id="metas_orks",
                        name="Metas/ORKs",
                        comments=None
                    ),
                    PrincipleModel(
                        id="desdobramentos_estrategicos",
                        name="Desdobramentos estratégicos",
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
