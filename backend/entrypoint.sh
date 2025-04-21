#!/bin/sh

# Define o comando padrão
DEFAULT_CMD="poetry run uvicorn src.main:app --host 0.0.0.0 --port ${INTERNAL_PORT}"

# Executa o comando padrão com quaisquer argumentos adicionais passados
exec $DEFAULT_CMD "$@"