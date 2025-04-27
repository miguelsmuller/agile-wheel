# Front End

## Variáveis de Ambiente

Se for usar o poetry utilize o arquivo .env do diretório. Caso esteja utilizando o Docker é necessário definir as variaveis de ambiente.

## Ambiente Local com NPM

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

## Ambiente Local com Docker

Gere a imagem atualizada do backend

```bash
docker build --target prod -t agile-whell-frontend .
docker build -t agile-whell-frontend .
```

Execute a imagem

```bash
docker run  -d \
-e INTERNAL_PORT=80 \
-p 4444:80 \
--name agile-whell-frontend \
agile-whell-frontend
``` 