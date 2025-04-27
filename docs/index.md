# Sobre o Projeto

O objetivo deste projeto é facilitar a **avaliação da maturidade ágil de times** por meio de uma visualização clara e acessível, utilizando o modelo do **Agile Wheel**.

Além disso, a aplicação foi desenvolvida para que a **dinâmica seja aplicada diretamente pela web**, tornando-se ideal para **times remotos ou distribuídos** que desejam realizar diagnósticos colaborativos de forma prática, visual e em tempo real.

🔍 **Principais características:**

- Permite times avaliarem sua maturidade em **quatro pilares essenciais da agilidade**.
- Geração de **gráficos radar** para visualização do progresso.
- Arquitetura robusta baseada em **Arquitetura Hexagonal**, promovendo desacoplamento e testabilidade.
- Totalmente compatível com **Python 3.12**, gerenciado com **Poetry** para consistência de ambiente.
- Pronto para uso local com comandos simples de execução, testes e linting.

# Visão Geral do Monorepo

Este repositório segue o formato **monorepo**, agrupando **duas aplicações independentes** que evoluem em conjunto:

| Caminho           | Tecnologia & Stack                          | Descrição                                                                                   |
|-------------------|---------------------------------------------|---------------------------------------------------------------------------------------------|
| `backend/`        | **Python 3.12** · FastAPI · Poetry          | API REST/GraphQL, regras de negócio, persistência e serviços externos.                      |
| `frontend/`       | **Angular 19** · TypeScript · Vite/ESBuild  | Interface web que consome a API, renderiza dashboards e gráficos interativos em tempo real. |

# Rodando o projeto

Já existe um `docker-compose` preparado para executar o conjunto de serviços localmente.

## Variáveis de Ambiente

Certifique-se de configurar as seguintes variáveis de ambiente antes de executar o projeto:

- Existe um arquivo `.env` na raiz do projeto, responsável por variáveis globais utilizadas pelo `docker-compose`. Essas variáveis são gerais e, teoricamente, não devem influenciar a lógica interna de nenhum serviço.
- Cada serviço possui suas próprias variáveis de ambiente específicas, que estão melhor descritas nas especificações individuais de cada serviço.
    - [Variáveis de Ambiente do backend](./backend/index.md)
    - [Variáveis de Ambiente do frontend](./frontend/index.md)

## Execução Local

Utilize o seguinte comando para iniciar os serviços:

```sh
docker compose up \
-d --force-recreate --build
```