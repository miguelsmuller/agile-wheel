# Backend

## Estrutura do Projeto (Arquitetura Hexagonal)

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

## Dependencia

É necessário ter um banco de dados para executar o backend

```bash
docker run -d \
--name mongo \
-p 27017:27017 \
-v mongo-data:/data/db \
mongo:latest
```

## Variáveis de Ambiente

Se for usar o poetry utilize o arquivo .env do diretório. Caso esteja utilizando o Docker é necessário definir as variaveis de ambiente.

## Ambiente Local com Poetry

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

## Ambiente Local com Docker

Gere a imagem atualizada do backend
```sh
docker build -t agile-whell-backend .
```

Execute a imagem
```sh
docker run  -d \
-e INTERNAL_PORT=8080 \
-e DB_HOST=host.docker.internal \
-e DB_PORT=27017 \
-p 3333:8080 \
--name agile-whell-backend \
agile-whell-backend
```

Para realizar algum debug pode executar

```sh
docker run -it agile-whell-backend sh
apt update && apt install -y iputils-ping curl dnsutils telnet
```
