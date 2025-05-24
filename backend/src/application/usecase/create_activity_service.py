from src.application.ports.input.create_activity_port import CreateActivityPort
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity
from src.domain.entities.dimension import Dimension, Principle
from src.domain.entities.participant import Participant


class CreateActivityService(CreateActivityPort):
    def __init__(self, repository: ActivityRepositoryPort = None):
        self.repository = repository

    async def execute(self, owner: Participant) -> Activity:
        activity = Activity()

        activity.is_opened = True

        self._add_default_dimenstions(activity)

        activity.add_participant(owner)

        return await self.repository.create(activity)

    def _add_default_dimenstions(self, activity: Activity) -> None:
        dimensions = [
            Dimension(
                id="experimente",
                name="Experimente e Aprenda Rápido",
                principles=[
                    Principle(
                        "compartilhamento_de_conhecimento",
                        "Compartilhamento de conhecimento"
                    ),
                    Principle("comprometimento_com_o_produto", "Comprometimento com o produto"),
                    Principle("praticas_lean_agile", "Práticas Lean-Agile"),
                    Principle("ritmo_das_entregas", "Ritmo das entregas"),
                    Principle("granularidade_de_demandas", "Granularidade de demandas"),
                ]
            ),
            Dimension(
                id="pessoas",
                name="Pessoas Sensacionais",
                principles=[
                    Principle("colaboracao_e_comunicacao", "Colaboração e comunicação"),
                    Principle("motivacao_e_confianca", "Motivação e confiança"),
                    Principle("autonomia_e_auto_organizacao", "Autonomia e auto-organização"),
                    Principle("melhoria_continua", "Melhoria Contínua"),
                    Principle("interdisciplinaridade", "Interdisciplinaridade"),
                ]
            ),
            Dimension(
                id="valor",
                name="Valor a Todo Instante",
                principles=[
                    Principle("discovery_upstream_kanban", "Discovery/Upstream Kanban"),
                    Principle("user_experience_ux_ui", "User Experience (UX/UI)"),
                    Principle("entrega_de_valor_percebido", "Entrega de valor (percebido)"),
                    Principle("relacionamento_com_o_negocio", "Relacionamento com o negócio"),
                    Principle("satisfacao_do_cliente", "Satisfação do cliente"),
                ]
            ),
            Dimension(
                id="seguranca",
                name="Segurança é um Pré-requisito",
                principles=[
                    Principle("trabalho_sustentavel", "Trabalho sustentável"),
                    Principle("metricas_ageis", "Métricas Ágeis"),
                    Principle("estimativas_e_contratos_ageis", "Estimativas & contratos ágeis"),
                    Principle("metas_orks", "Metas/ORKs"),
                    Principle("desdobramentos_estrategicos", "Desdobramentos estratégicos"),
                ]
            )
        ]

        for dimension in dimensions:
            activity.add_dimension(dimension)
