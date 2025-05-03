# Backend

Este documento fornece uma visão geral do componente backend para o aplicativo Agile Wheel. A API serve atualmente como ponto de integração entre a camada de apresentação e a camada de persistência, gerenciando todas as operações de dados por meio de uma interface RESTful desenvolvida com Python/FastAPI.

Para obter informações sobre a arquitetura geral do backend e os princípios de design, consulte [Arquitetura do backend](../1-architecture/index.md).

## Visão geral da API

A API de backend do Agile Wheel segue uma arquitetura hexagonal (padrão de portas e adaptadores) para manter a separação de interesses entre a lógica de domínio e as interfaces externas. A camada de API atua como um adaptador de entrada que transforma solicitações HTTP em operações de domínio.

```mermaid
flowchart TB
    HTTP["HTTP Endpoints"] --> Schemas["Request/Response Schemas"]
    Schemas --> InputPorts["Input Ports"]
    InputPorts --> UseCases["Use Cases/Services"]
    UseCases --> DomainEntities["Domain Entities"]
    UseCases --> OutputPorts["Output Ports"]
    OutputPorts --> Repositories["MongoDB Repositories"]
    Repositories --> DB["MongoDB"]

    subgraph API Layer
        HTTP
        Schemas
        InputPorts
    end

    subgraph Application Core
        UseCases
        DomainEntities
        OutputPorts
    end

    subgraph Repository Layer
        Repositories
        DB
    end
```

## Pontos de extremidade da API

O backend fornece vários endpoints RESTful para o aplicativo Agile Wheel:

```mermaid
flowchart LR
    POST_Activity["POST /activity"] -->|Creates new activity| CreateActivityService["CreateActivityService"]
    GET_Activity["GET /activity/{id}"] -->|Retrieves activity| ValidateActivityService["ValidateActivityService"]
    POST_Join["POST /activity/{id}/join"] -->|Joins an activity| JoinActivityService["JoinActivityService"]
    POST_Close["POST /activity/{id}/close"] -->|Closes an activity| CloseActivityService["CloseActivityService"]
    POST_Evaluate["POST /activity/{id}/evaluate"] -->|Evaluates principles| EvaluateActivityService["EvaluateActivityService"]
    GET_Ping["GET /ping"] -->|Health check| PingService["PingService"]

    CreateActivityService -->|Creates| ActivityEntity["Activity Entity"]
    ValidateActivityService -->|Validates| ActivityEntity
    JoinActivityService -->|Updates| ActivityEntity
    CloseActivityService -->|Updates| ActivityEntity
    EvaluateActivityService -->|Adds data to| ActivityEntity

    ActivityEntity -->|Stored in| MongoDB["MongoDB Database"]

    subgraph FastAPI_Application
        POST_Activity
        GET_Activity
        POST_Join
        POST_Close
        POST_Evaluate
        GET_Ping
        CreateActivityService
        ValidateActivityService
        JoinActivityService
        CloseActivityService
        EvaluateActivityService
        PingService
    end

    subgraph Activity_Domain
        ActivityEntity
    end
```

### Tabela de resumo de endpoints

| Endpoint                  | Method | Description                                 | Request Schema          | Response Schema          |
|---------------------------|--------|---------------------------------------------|-------------------------|--------------------------|
| `/activity`               | POST   | Creates a new Agile Wheel activity          | `CreateActivityRequest` | `CreateActivityResponse` |
| `/activity/{id}`          | GET    | Retrieves an existing activity              | -                       | `StatusResponse`         |
| `/activity/{id}/join`     | POST   | Joins an existing activity as a participant | `JoinRequest`           | `JoinResponse`           |
| `/activity/{id}/close`    | POST   | Closes an activity for further evaluations  | -                       | `CloseResponse`          |
| `/activity/{id}/evaluate` | POST   | Submits evaluations for principles          | `EvaluationRequest`     | `EvaluationResponse`     |
| `/ping`                   | GET    | Health check endpoint                       | -                       | `PongResponse`           |


## Request and Response Schemas

A API utiliza modelos Pydantic para validação e serialização de dados de solicitação/resposta. Esses esquemas funcionam como um contrato entre o front-end e o back-end.

### Core Response Models

Esses modelos representam as entidades de domínio quando retornados em respostas de API:

```mermaid
classDiagram
    class ActivityResponse {
        +str activity_id
        +datetime created_at
        +bool is_opened
        +str owner_name
        +list~ParticipantResponse~ participants
        +list~DimensionResponse~ dimensions
        +from_activity(activity) ActivityResponse
    }

    class ParticipantResponse {
        +str id
        +str name
        +str email
        +from_participant(participant) ParticipantResponse
    }

    class DimensionResponse {
        +str id
        +str dimension
        +str comments
        +list~PrincipleResponse~ principles
        +from_dimension(dimension) DimensionResponse
    }

    class PrincipleResponse {
        +str id
        +str principle
        +str comments
        +from_principle(principle) PrincipleResponse
    }

    ActivityResponse --> "list" ParticipantResponse : contains
    ActivityResponse --> "list" DimensionResponse : contains
    DimensionResponse --> "list" PrincipleResponse : contains
```

### Request Schemas e Response Schemas

Os seguintes esquemas são usados ​​para solicitações de entrada:

??? "backend/src/adapters/input/schemas.py"

    ```python title="backend/src/adapters/input/http/schemas.py"
    --8<-- "./backend/src/adapters/input/http/schemas.py"
    ```

## API Implementation Pattern

A implementação da API segue um padrão consistente usando o sistema de injeção de dependência do FastAPI:

```mermaid
flowchart TD

    subgraph FastAPI_Endpoint ["FastAPI Endpoint"]
        EP["@router.post(...)"]
        RequestSchema["Request Schema Validation"]
        UC["Use Case/Service Injection"]
        DomainMapping["Map to Domain Entities"]
        ExecuteUseCase["Execute Use Case"]
        ResponseMapping["Map Domain to Response"]
        Return["Return Response"]
    end

    subgraph Domain_Layer ["Domain Layer"]
        DomainLogic["Domain Logic/Services"]
        Repository["Repository Operations"]
    end

    subgraph Database_Layer ["Database Layer"]
        MongoDB["MongoDB"]
    end

    EP --> RequestSchema
    RequestSchema --> UC
    UC --> DomainMapping
    DomainMapping --> ExecuteUseCase
    ExecuteUseCase --> ResponseMapping
    ResponseMapping --> Return
    ExecuteUseCase --> DomainLogic
    DomainLogic --> Repository
    Repository --> MongoDB
```

Exemplo de implementação da base de código:

??? "backend/src/adapters/input/router.py"

    ```python title="backend/src/adapters/input/router.py"
    --8<-- "./backend/src/adapters/input/router.py"
    ```

## API Dependencies and Configuration

A API de backend depende de diversas dependências definidas na configuração do projeto:

| Dependency        | Version                   | Purpose                              |
|-------------------|---------------------------|--------------------------------------|
| FastAPI           | &gt;=0.115.12,&lt;0.116.0 | Web framework for building APIs      |
| Uvicorn           | &gt;=0.34.0,&lt;0.35.0    | ASGI server for FastAPI              |
| Pydantic          | &gt;=2.11.2,&lt;3.0.0     | Data validation and serialization    |
| Beanie            | &gt;=1.29.0,&lt;2.0.0     | MongoDB ODM (Object Document Mapper) |
| Motor             | &gt;=3.7.0,&lt;4.0.0      | Async MongoDB driver                 |
| Pydantic-settings | &gt;=2.8.1,&lt;3.0.0      | Settings management with Pydantic    |


## API Deployment

A API é conteinerizada usando o Docker e pode ser implantada como parte da pilha completa do aplicativo:

```mermaid
flowchart TD

    subgraph Docker_Container["Docker Container"]
        Python["Python 3.12 Runtime"]
        Poetry["Poetry Package Manager"]
        Dependencies["Install Dependencies"]
        UvicornServer["Uvicorn ASGI Server"]
        FastAPI["FastAPI Application"]
    end

    subgraph External_Dependencies["External Dependencies"]
        MongoDB["MongoDB Database"]
    end

    Client["HTTP Client/Frontend"]

    Python --> Poetry
    Poetry --> Dependencies
    Dependencies --> UvicornServer
    UvicornServer --> FastAPI
    FastAPI --> MongoDB
    Client --> UvicornServer
```

O contêiner do Docker expõe a porta 8000 internamente, que pode ser mapeada para qualquer porta externa ao executar o contêiner.

Configuração de chaves no Dockerfile:

- Usa imagem slim do Python 3.12.0
- Instala dependências via Poetry
- Expõe porta interna configurável
- Executa o aplicativo usando Uvicorn

## API Error Handling

A API lida com erros por meio do sistema de exceções do FastAPI, retornando códigos de status HTTP apropriados:

| Error Condition       | HTTP Status               | Response                 |
|-----------------------|---------------------------|--------------------------|
| Invalid request data  | 422 Unprocessable Entity  | Validation error details |
| Activity not found    | 404 Not Found             | Error message            |
| Activity closed       | 400 Bad Request           | Error message            |
| Duplicate participant | 400 Bad Request           | Error message            |
| Server error          | 500 Internal Server Error | Error message            |

O FastAPI valida automaticamente os dados de solicitação usando os modelos Pydantic, reduzindo a necessidade de código de validação explícito nos endpoints.

