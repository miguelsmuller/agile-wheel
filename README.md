[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=miguelsmuller_agile-wheel&metric=alert_status&token=38a3a1ccb5d8516794cdfb557cd8c292ce57cc71)](https://sonarcloud.io/summary/new_code?id=miguelsmuller_agile-wheel) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=miguelsmuller_agile-wheel&metric=reliability_rating&token=38a3a1ccb5d8516794cdfb557cd8c292ce57cc71)](https://sonarcloud.io/summary/new_code?id=miguelsmuller_agile-wheel) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=miguelsmuller_agile-wheel&metric=coverage&token=38a3a1ccb5d8516794cdfb557cd8c292ce57cc71)](https://sonarcloud.io/summary/new_code?id=miguelsmuller_agile-wheel) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=miguelsmuller_agile-wheel&metric=sqale_rating&token=38a3a1ccb5d8516794cdfb557cd8c292ce57cc71)](https://sonarcloud.io/summary/new_code?id=miguelsmuller_agile-wheel)

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

---

## 🗂️ Visão Geral do Monorepo

Este repositório segue o formato **monorepo**, agrupando **duas aplicações independentes** que evoluem em conjunto:

| Caminho           | Tecnologia & Stack                          | Descrição                                                                                   |
|-------------------|---------------------------------------------|---------------------------------------------------------------------------------------------|
| `backend/`        | **Python 3.12** · FastAPI · Poetry          | API REST/GraphQL, regras de negócio, persistência e serviços externos.                      |
| `frontend/`       | **Angular 19** · TypeScript · Vite/ESBuild  | Interface web que consome a API, renderiza dashboards e gráficos interativos em tempo real. |

Ambos os diretórios possuem seus próprios **.gitignore** e scripts, mas partilham um único `pyproject.toml` e `package.json` na raiz, simplificando a instalação de dependências e a automação em CI/CD.

> **Pré‑requisitos globais**  
> • **Python 3.12+** — recomendado via `pyenv`  
> • **Node ≥ 18.19 (LTS 20 recomendado)** — recomendado via `nvm`

---

# Backend

## 📦 Ambiente Local com Poetry (Backend)

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

---

## 🧱 Estrutura do Projeto (Arquitetura Hexagonal)

O projeto segue o padrão da **Arquitetura Hexagonal (Ports and Adapters)**, com uma separação clara entre as regras de negócio e as camadas externas (como banco de dados, APIs, interfaces, etc).

Estrutura básica:

```sh
.
├── backend
│   ├── src
│   │   ├── adapters
│   │   │   └── input/output
│   │   ├── domain
│   │   │   └── entities
│   │   ├── application
│   │   │   ├── ports
│   │   │   │   └── input/output
│   │   │   └── usecase
│   │   └── config
│   └── tests
│
├── frontend
│   ├── src
│   └── angular.json
│
├── pyproject.toml
├── package.json
└── compose.yaml
```

Essa organização facilita a escalabilidade, testabilidade e manutenção do projeto, mantendo as regras de negócio isoladas de frameworks e tecnologias externas.

---

# Front End

## 📦 Ambiente Local com NPM (Frontend)

> Todos os comandos a seguir são executados **na raiz** do repositório graças ao suporte a **npm workspaces**.

```bash
# 1. Garanta Node >= 18.19 (ou use `nvm install 20 && nvm use 20`)
# 2. Instale dependências de todos os workspaces (frontend)
npm install

# 3. Suba o servidor de desenvolvimento Angular em http://localhost:4200
npm run start            # alias: npm run start --workspace frontend

# 4. Outros scripts úteis
a) npm run build         # build de produção do Angular
b) npm run test          # testes unitários Karma/Jasmine
```

**Estrutura de comandos** (definidos em `package.json` raiz):

| Comando                 | Faz o quê?                               |
|-------------------------|-------------------------------------------|
| `npm run start`         | `ng serve` dentro de `frontend/`.         |
| `npm run build`         | `ng build` dentro de `frontend/`.         |
| `npm run test`          | `ng test` dentro de `frontend/`.          |

