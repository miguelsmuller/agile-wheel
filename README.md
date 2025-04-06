# Agile Wheel

## 🧠 O que é o Agile Wheel?

O **Agile Wheel** é uma abordagem visual de medição da maturidade ágil, organizada em quatro pilares:

1. **Pessoas Sensacionais**
2. **Experimente e Aprenda Rápido**
3. **Segurança é um Pré-requisito**
4. **Valor a Todo Instante**

Cada dinâmica permite que times avaliem sua maturidade por meio de notas ou distribuição de pontos, com visualização final em um **Gráfico Radar**.





## 📦 Ambiente Local com Poetry

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
poetry@aw run ruff check .
poetry@aw run mypy src/
```



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
