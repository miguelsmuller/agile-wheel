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

1. **Configure o Poetry para criar ambientes virtuais dentro do projeto** (útil para manter tudo isolado):

```bash
poetry config virtualenvs.in-project true
```

2. **Defina a versão do Python a ser utilizada**:

```bash
poetry env use 3.11
```

3. **Instale as dependências do projeto**:

```bash
poetry install
```

4. **Execute comandos usando o Poetry local**:

```bash
./poetry.sh run <comando>
```

5. **Rodando o projet**:

```bash
./poetry.sh run uvicorn src.entrypoints.http.main:app --reload
```


---

## 🧱 Estrutura do Projeto (Arquitetura Hexagonal)

O projeto segue o padrão da **Arquitetura Hexagonal (Ports and Adapters)**, com uma separação clara entre as regras de negócio e as camadas externas (como banco de dados, APIs, interfaces, etc).

Estrutura básica:

```shell
.
├── src
│   ├── adapters
│   │   └── in/out
│   ├── application
│   ├── config
│   ├── domain
│   ├── entrypoints
│   │   ├── consumer
│   │   └── http
│   └── ports
│       └── in/out
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
