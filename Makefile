CONTAINER_ENGINE := $(shell which podman || which docker)
COMPOSE := $(CONTAINER_ENGINE) compose

ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: run
run: ## Run the project.
	poetry run python -m src.main

.PHONY: install
install: ## Install Python package dependencies.
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root
	poetry run pre-commit install

.PHONY: test
test: ## Run automated tests.
	ENVIRONMENT=test poetry run pytest --cov

.PHONY: up
up: ## Start all containers.
	$(COMPOSE) -f ./docker-compose.yml up -d --force-recreate

.PHONY: recreate
recreate: ## Recreate all containers.
	$(COMPOSE) -f ./docker-compose.yml up -d --force-recreate --build

.PHONY: up-database
up-database: ## Start database container.
	$(COMPOSE) -f ./docker-compose.yml up -d sso-db --force-recreate

.PHONY: down
down: ## Stop all containers.
	$(COMPOSE) down

.PHONY: revision
revision: ## Create a new database revision following the repository's models.
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

.PHONY: migrate
migrate: ## Run database migrations.
	poetry run alembic upgrade head

.PHONY: downgrade
downgrade: ## Undo last database migration.
	poetry run alembic downgrade -1

.PHONY: remove-containers
remove-containers: ## Remove all containers.
	$(CONTAINER_ENGINE) rm -f $$($(CONTAINER_ENGINE) ps -a -q)

.PHONY: remove-container-images
remove-container-images: ## Remove all downloaded container images.
	$(CONTAINER_ENGINE) rmi -f $$($(CONTAINER_ENGINE) images -q)

.PHONY: export-requirements
export-requirements: ## Export poetry managed packages to a requirements.txt (needed by Vercel).
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: pre-commit
pre-commit: ## Run pre-commit checks.
	poetry run pre-commit run --config ./.pre-commit-config.yaml

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release).
	poetry version patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release).
	poetry version minor

.PHONY: major
major: ## Bump project version to next major (breaking change).
	poetry version major

.PHONY: generate-secret-key
generate-secret-key: ## Generate a new secret key.
	poetry run python -c 'import secrets; print(secrets.token_hex(32))'

.PHONY: init-env
init-env: ## Copy .env.example to .env and populate SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES.
	@if [ -f .env ]; then \
		echo "Error: .env already exists. Aborting."; \
		exit 1; \
	fi;

	@if [ -f .env.docker ]; then \
		echo "Error: .env.docker already exists. Aborting."; \
		exit 1; \
	fi;

	@cp .env.example .env
	@cp .env.docker.example .env.docker
	@sed -i '' -e '/^SECRET_KEY=/d' -e '/^ALGORITHM=/d' -e '/^ACCESS_TOKEN_EXPIRE_MINUTES=/d' .env
	@sed -i '' -e '/^SECRET_KEY=/d' -e '/^ALGORITHM=/d' -e '/^ACCESS_TOKEN_EXPIRE_MINUTES=/d' .env.docker

	@SECRET_KEY=$$( \
		if command -v python >/dev/null 2>&1; then \
			python -c 'import secrets; print(secrets.token_hex(32))'; \
		elif command -v node >/dev/null 2>&1; then \
			node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"; \
		elif command -v openssl >/dev/null 2>&1; then \
			openssl rand -hex 32; \
		fi \
	); \
	if [ -z "$$SECRET_KEY" ]; then \
		echo "Error: Failed to generate SECRET_KEY. Aborting."; \
		exit 1; \
	fi; \
	echo "SECRET_KEY=$$SECRET_KEY" | tee -a .env .env.docker > /dev/null

	@echo "ALGORITHM=HS256" >> .env
	@echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env
	@echo "ALGORITHM=HS256" >> .env.docker
	@echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env.docker

.PHONY: clean
clean: ## Clean project's temporary files.
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
