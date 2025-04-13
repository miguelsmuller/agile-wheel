# Agile Wheel

## 🧠 O que é o Agile Wheel?

O **Agile Wheel** é uma abordagem visual de medição da maturidade ágil, idealizada por **[Ana G. Soares](https://www.linkedin.com/in/anagsoares/)**, organizada em quatro pilares:

1. **Pessoas Sensacionais**
    - Colaboração e comunicação
    - Motivação e confiança
    - Autonomia e auto-organização
    - Melhoria Contínua
    - Interdisciplinaridade

2. **Experimente e Aprenda Rápido**
    - Compartilhamento de conhecimento
    - Comprometimento com o produto
    - Práticas Lean-Agile
    - Ritmo das entregas
    - Granularidade de demandas

3. **Segurança é um Pré-requisito**
    - Trabalho sustentável
    - Métricas Ágeis
    - Estimativas & contratos ágeis
    - Metas/ORKs
    - Desdobramentos estratégicos

4. **Valor a Todo Instante**
    - Discovery/Upstream Kanban
    - User Experience (UX/UI)
    - Entrega de valor (percebido)
    - Relacionamento com o negócio
    - Satisfação do cliente

![Agile Wheel - Roda Ágil - Exemplo](<docs/assets/Agile Wheel - Roda Ágil by Ana G. Soares - Exemplo.jpg>)

## 🚀 Sobre o Projeto

O objetivo deste projeto é facilitar a **avaliação da maturidade ágil de times** por meio de uma visualização clara e acessível, utilizando o modelo do **Agile Wheel**.

Além disso, a aplicação foi desenvolvida para que a **dinâmica seja aplicada diretamente pela web**, tornando-se ideal para **times remotos ou distribuídos** que desejam realizar diagnósticos colaborativos de forma prática, visual e em tempo real.

🔍 **Principais características:**

- Permite times avaliarem sua maturidade em **quatro pilares essenciais da agilidade**.
- Geração de **gráficos radar** para visualização do progresso.
- Arquitetura robusta baseada em **Arquitetura Hexagonal**, promovendo desacoplamento e testabilidade.
- Totalmente compatível com **Python 3.12**, gerenciado com **Poetry** para consistência de ambiente.
- Pronto para uso local com comandos simples de execução, testes e linting.


## 📦 Ambiente Local com Poetry

### 1. Instale o Python 3.12 (usando pyenv recomendado)

```bash
pyenv install 3.12.0
```


### 2. Instale o Poetry com sufixo (via pipx)

```bash
pipx install --suffix "@aw" poetry==2.1.1 --python python3.12
# Isso criará o comando poetry@aw disponível globalmente, vinculado à versão correta do Python e do Poetry.
```


### 3. Crie e use o ambiente virtual

```bash
poetry config virtualenvs.in-project true
poetry@aw env use 3.12
poetry@aw install
```


### 4. Executando o Projeto

```bash
# Rodar aplicação localmente
poetry poe serve
# ou
poetry@aw run uvicorn src:app --reload

# Rodar testes, linters, etc
poetry@aw run pytest
poetry@aw run pytest --cov=src
poetry@aw run pytest --cov=src --cov-report=html
poetry@aw run ruff check .
poetry@aw run mypy src/
```



## 🧱 Estrutura do Projeto (Arquitetura Hexagonal)

O projeto segue o padrão da **Arquitetura Hexagonal (Ports and Adapters)**, com uma separação clara entre as regras de negócio e as camadas externas (como banco de dados, APIs, interfaces, etc).

Estrutura básica:

```sh
.
├── src
│   ├── adapters
│   │   └── input/output
│   ├── domain
│   │   └── entities
│   ├── application
│   │   ├── ports
│   │   │   └── input/output
│   │   └── usecase
│   └── config
│
├── tests
│   └── ...
│
├── README.md
├── poetry.sh
├── pyproject.toml
└── compose.yaml
```

Essa organização facilita a escalabilidade, testabilidade e manutenção do projeto, mantendo as regras de negócio isoladas de frameworks e tecnologias externas.
