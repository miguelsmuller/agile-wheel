# Execução Local

> [!NOTE]  
> Para facilitar o setup é bom entender que o projeto possui automações já disponíveis (Makefile, Python e Poetry, integrações com VSCode, etc), leia primeiro a documentação: [automations.md](./automations.md).

## Executando o Conjunto de Componentes

O aplicativo pode ser executado localmente usando o Docker Compose:

```sh
docker compose up -d --force-recreate --build
```

Este comando inicia todos os serviços necessários em contêineres com a configuração default.

Para desenvolvimento de componentes individuais:

## Executando apenas backend

Ainda vai ser necessário ter um banco de dados para executar o backend

```sh
docker run -d \
--name mongo \
-p 27017:27017 \
-v mongo-data:/data/db \
mongo:latest
```

1. Instale o Python 3.12 (usando pyenv recomendado)

```sh
cd backend  # Dentro do diretório do backend
```

```sh
pyenv install 3.12.0
```

2. Instale o Poetry com sufixo (via pipx)

```sh
pipx install --suffix "@aw" poetry==2.1.1 --python "$(pyenv prefix 3.12.0)/bin/python"
# Isso criará o comando poetry@aw disponível globalmente
# O comando está vinculado à versão correta do Python e do Poetry.
```

3. Crie e use o ambiente virtual

```sh
poetry config virtualenvs.in-project true
poetry@aw env use 3.12.0
poetry@aw install
poetry@aw run uvicorn src.main:app --port 3333 --reload
```

4. Executando o Projeto

```sh
# Rodar aplicação localmente
poetry run poe serve
# ou
poetry@aw run uvicorn src.main:app --port 3333 --reload

# Rodar testes, linters, etc
poetry@aw run pytest
poetry@aw run pytest --cov=src
poetry@aw run pytest --cov=src --cov-report=html
poetry@aw run ruff check .
poetry@aw run mypy src/
```

### Backend Local com Docker

1. Gere a imagem atualizada do backend

```sh
docker build -t agile-whell-backend .
```

2. Execute a imagem

```sh
docker run  -d \
-e INTERNAL_PORT=8080 \
-e DB_HOST=host.docker.internal \
-e DB_PORT=27017 \
-e ALLOWED_ORIGINS="*" \
-p 3333:8080 \
--name agile-whell-backend \
agile-whell-backend
```

3. Para realizar algum debug pode executar

```sh
docker run -it agile-whell-backend sh
apt update && apt install -y iputils-ping curl dnsutils telnet
```

## Exceutando apenas frontend

```sh
cd frontend

nvm install 22
nvm use 22
npm install

npm run
```

Acesso na porta padrão 4200 do angular: http://localhost:4200

### Frontend Local com Docker

1. Gere a imagem atualizada do backend

```sh
docker build --target prod -t agile-whell-frontend .
```

2. Execute a imagem

```sh
docker run  -d \
-e INTERNAL_PORT=80 \
-e PRODUCTION=false \
-e API_AGILEWHEEL_URL=http://localhost \
-e WS_AGILEWHEEL_URL=ws://localhost \
-p 4444:80 \
--name agile-whell-frontend \
agile-whell-frontend
``` 

Acesso na porta exposta pelo docker: http://localhost:4444