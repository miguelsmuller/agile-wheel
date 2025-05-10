.SILENT:

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m

PROJECT_NAME = `basename $(PWD)`

## prints this help
help:
	printf "${COLOR_YELLOW}\n${PROJECT_NAME}\n\n${COLOR_RESET}"
	awk '/^[a-zA-Z0-9\.\-]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if ($$1 !~ /^\./) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "${COLOR_GREEN}$$ make %s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	printf "\n"

## generates .env files for backend and frontend if they don't exist
.generate_env:
	@echo "Generating .env files if they don't exist..."
	[ -f .env ] || cp .env.template .env
	[ -f backend/.env ] || cp backend/.env.template backend/.env
	[ -f frontend/.env ] || cp frontend/.env.template frontend/.env

## sets up the project locally using Docker containers
install-locally: .generate_env
	@echo "Setting up the project locally..."
	docker compose up -d --force-recreate --build --remove-orphans

## starts the project services in Docker containers
compose-up:
	docker compose up -d --force-recreate --build --remove-orphans

## stops and removes the project services in Docker containers
compose-down:
	docker compose down