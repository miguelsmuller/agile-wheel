# Usa uma imagem base oficial do Python
FROM python:3.12.0-slim

# Instala o Poetry
RUN pip install --no-cache-dir poetry

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia apenas os arquivos necessários para instalar as dependências
COPY pyproject.toml poetry.lock ./

# Copia o restante do código do projeto para o contêiner
COPY README.md .
COPY src ./src

# Instala as dependências do projeto sem criar um ambiente virtual
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Define uma variável de ambiente para a porta
ENV PORT=8000

# Expõe a porta padrão do FastAPI
EXPOSE ${PORT}

# Comando para iniciar o servidor FastAPI usando Uvicorn
CMD ["sh", "-c", "poetry run uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]