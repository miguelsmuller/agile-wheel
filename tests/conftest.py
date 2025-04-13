from datetime import datetime
from uuid import UUID

import pytest
import pytz
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient
from src.adapters.output.activity_document_mongo import ActivityDocument
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

mock_activity_uuid = UUID("b3d59547-35fc-446d-b567-8ba6ab65f764")
mock_activity_created = datetime(
    2025, 4, 13, 10, 30, 00, 00, tzinfo=pytz.timezone("America/Sao_Paulo")
)

@pytest.fixture
def mock_activity_fixture():
    return Activity(
        id=mock_activity_uuid,
        opened=False,
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
