.SILENT:

COLOR_RESET = \033[0m
COLOR_BOLD = \033[1m
COLOR_GREEN = \033[32m
COLOR_GREEN_BOLD = \033[1;32m
COLOR_RED = \033[31m
COLOR_RED_BOLD = \033[1;31m
COLOR_YELLOW = \033[33m
COLOR_YELLOW_BOLD = \033[1;33m

PROJECT_NAME = `basename $(PWD)`

# include .env.local
# export $(shell sed 's/=.*//' .env.local)

export PATH := $(HOME)/.local/bin:$(PATH)

.PHONY: help
help: ## Command help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: generate_env
generate_env:
	@echo "Generating .env files if they don't exist..."
	[ -f .env ] || cp .env.template .env
	[ -f backend/.env ] || cp backend/.env.template backend/.env
	[ -f frontend/.env ] || cp frontend/.env.template frontend/.env


.PHONY: compose-build
compose-build: ## sets up the project locally using Docker containers
	$(MAKE) --no-print-directory generate_env
	@echo "Setting up the project locally..."
	docker compose build --no-cache


.PHONY: compose-up
compose-up: ## starts the project services in Docker containers
	@echo "Starting the project services..."
	docker compose up -d --force-recreate --remove-orphans


.PHONY: compose-down
compose-down: ## stops and removes the project services in Docker containers
	@echo "Stopping and removing the project services..."
	docker compose down


.PHONY: test
test: ## runs tests for both backend and frontend
	@printf "${COLOR_GREEN_BOLD}Running tests for both backend and frontend...${COLOR_RESET}"
	@echo "\n"
	$(MAKE) --no-print-directory backend-test


.PHONY: lint
lint: ## runs linters for both backend and frontend
	@printf "${COLOR_GREEN_BOLD}Running linters for both backend and frontend...${COLOR_RESET}"
	@echo "\n"
	$(MAKE) --no-print-directory backend-lint
	@echo "\n"
	$(MAKE) --no-print-directory lint-frontend


.PHONY: lint-frontend
frontend-lint: ## run linter for frontend
	@printf "${COLOR_GREEN_BOLD}Running linter for frontend...${COLOR_RESET}"
	@echo "\n"
	docker compose exec frontend npm run lint


.PHONY: backend-lint
backend-lint: ## run linter for backend
	@printf "${COLOR_GREEN_BOLD}Running linter for backend...${COLOR_RESET}"
	@echo "\n"
	docker compose exec backend poetry run poe lint


.PHONY: backend-test
backend-test: ## runs tests for backend
	@printf "${COLOR_GREEN_BOLD}Running tests for backend...${COLOR_RESET}"
	@echo "\n"
	docker compose exec backend poetry run poe test


.PHONY: backend-exec
backend-exec: ## run the backend shell
	@printf "${COLOR_GREEN_BOLD}Exec container shell...${COLOR_RESET}"
	@echo "\n"
	docker compose exec backend /bin/bash


.PHONY: backend-logs
backend-logs: ## display logs from the backend
	@printf "${COLOR_GREEN_BOLD}Backend logs...${COLOR_RESET}"
	@echo "\n"
	docker compose logs backend -f

.PHONY: backend-dep-install
backend-dep-install: ## install backend dependencies
	@printf "${COLOR_GREEN_BOLD}Install dependencies for backend...${COLOR_RESET}"
	@echo "\n"
	docker compose exec backend poetry run poe dep-install

.PHONY: backend-dep-update
backend-dep-update: ## update backend dependencies
	@printf "${COLOR_GREEN_BOLD}Update dependencies for backend...${COLOR_RESET}"
	@echo "\n"
	docker compose exec backend poetry run poe dep-update

.PHONY: backend-dep-lock
backend-dep-lock: ## lock backend dependencies
	@printf "${COLOR_GREEN_BOLD}Lock file for backend...${COLOR_RESET}"
	@echo "\n"
	docker compose exec backend poetry run poe dep-lock