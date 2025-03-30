# Agile Wheel

Este projeto utiliza uma abordagem que encapsula o **Poetry** como uma dependência local do próprio repositório, evitando problemas de incompatibilidade entre versões globais diferentes do Poetry instaladas no sistema.  
Para isso, existe um script chamado `poetry.sh` na raiz do projeto, garantindo que sempre seja utilizada a **versão local do Poetry**.

> ⚠️ Ainda assim, é necessário ter o **Poetry instalado globalmente** para iniciar o projeto e instalar as dependências locais corretamente.

---

## 📦 Ambiente Local com Poetry

Para utilizar o Poetry do próprio projeto, execute os comandos através do script:

```bash
./poetry.sh <comando>
```

Exemplo:

```bash
./poetry.sh --version
Poetry (version 2.1.2)

./poetry.sh run python --version
Python 3.11.6
```

---

## 🚀 Iniciando o Projeto

```sh
# Configure o Poetry para criar ambientes virtuais dentro do projeto
poetry config virtualenvs.in-project true

# Defina a versão do Python a ser utilizada
poetry env use 3.11

# Instale o Poetry na versão adequada
pip install "poetry==2.1.2"

# Instale as dependências do projeto
poetry install

# Execute comandos usando o Poetry local
./poetry.sh run <comando>

# Rodando o projet
./poetry.sh run uvicorn src:app --reload

```



---

## 🧱 Estrutura do Projeto (Arquitetura Hexagonal)

O projeto segue o padrão da **Arquitetura Hexagonal (Ports and Adapters)**, com uma separação clara entre as regras de negócio e as camadas externas (como banco de dados, APIs, interfaces, etc).

Estrutura básica:

```sh
.
├── src
│   ├── adapters
│   │   └── input/output
│   ├── application
│   │   ├── domain
│   │   │   └── models
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
