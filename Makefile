ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: run
run: ## Run the project.
	poetry run python -m api

.PHONY: install
install: ## Install Python requirements.
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root
	poetry run pre-commit install

.PHONY: test
test: ## Run tests.
	ENVIRONMENT=test poetry run pytest --cov

.PHONY: up-database
up-database: ## Start database container.
	docker compose up -d postgres --force-recreate

.PHONY: down
down: ## Stop all containers.
	docker compose down

.PHONY: migrate
migrate: ## Run database migrations.
	poetry run alembic upgrade head

.PHONY: revision
revision: ## Create a new database migration.
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

.PHONY: docker-rm
docker-rm: ## Remove all containers.
	docker rm -f $$(docker ps -a -q)

.PHONY: docker-rmi
docker-rmi: ## Remove all images.
	docker rmi -f $$(docker images -q)

.PHONY: pre-commit
pre-commit: ## Run pre-commit checks.
	poetry run pre-commit run --config ./.pre-commit-config.yaml

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release/chores).
	poetry version patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release).
	poetry version minor

.PHONY: clean
clean: ## Clean project's temporary files.
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
