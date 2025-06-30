# Automações Úteis

O projeto conta com automações e comandos prontos para facilitar a execução e manutenção do ambiente de desenvolvimento. A nível de raiz, há um **Makefile** com diversas tarefas úteis, abrangendo desde a execução completa do projeto até automações específicas para backend e frontend.

## Comandos raiz com Makefile

O arquivo [**Makefile**](../Makefile) na raiz do projeto concentra automações que facilitam o setup, build, execução, testes e manutenção global do projeto. Consulte este arquivo para entender todos os comandos disponíveis, suas descrições e sugestões de uso rápido para tarefas recorrentes de desenvolvimento.

```sh
$ make

# output
# compose-build        sets up the project ...
# compose-down         stops and removes the ...
# ...
# help                 Command help
# lint                 runs linters for both ...
# test                 runs tests for both ...
```

## Automações dos Componentes

Cada parte do projeto tem suas próprias automações internas. Os comandos devem ser executados dentro do diretório correspondente (backend ou frontend).

### Backend (`backend/`)

O [**pyproject.toml**](../backend/pyproject.toml) define as tasks do Poe the Poet usadas no backend. Nele, você encontra todas as automações disponíveis para rodar servidor local, testes, linters e gerenciamento de dependências Python. Explore a seção [tool.poe.tasks] para criar, editar ou consultar comandos automatizados específicos do backend.

```sh
$ poetry

# output
# Poetry (version 2.1.3)

# Usage:
#   command [options] [arguments]
#
# ...
#
# Available commands:
#   ...
#
#  poe
#   poe dep-install    
#   poe serve          
#   poe lint           
#   poe test           
#  ...
```

### Frontend (`frontend/`)

O [**package.json**](../frontend/package.json) traz todos os scripts npm disponíveis para desenvolvimento do frontend Angular. Ali estão os comandos essenciais para build, start, lint e testes da interface, além de eventuais scripts personalizados usados na rotina do projeto.

```sh
$ npm run

# output
# Lifecycle scripts included in front@0.0.0:
#   start
#     npm run prebuild && ng serve
#   ...

# available via `npm run-script`:
#   prebuild
#     node scripts/generate-env.mjs
#   ...
```


## Integração com VSCode

Arquivos `tasks.json` em `./.vscode`, `backend/.vscode` e `frontend/.vscode` já vêm prontos para integração com o Visual Studio Code. Eles permitem executar tarefas frequentes do Makefile, Poetry/Poe e npm diretamente do menu de tarefas do editor, facilitando o fluxo de trabalho e padronizando a experiência entre membros do time.
