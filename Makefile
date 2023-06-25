.PHONY: create-venv compile-requirements sync-requirements tox lint help

# Colors
PURPLE = \033[0;35m
GREEN = \033[0;32m
NC = \033[0m

# Separator
SEPARATOR = $============================================================================================$(NC)

# Default target
default: help

help:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Docker options:$(NC)"
	@echo "$(SEPARATOR)"
	@echo "  $(GREEN)make run-lexer-docker$(NC)      Creates a docker to run the lexer script."
	@echo "  $(GREEN)make run-parser-docker$(NC)     Creates a docker to run the parser script."
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Local options:$(NC)"
	@echo "$(SEPARATOR)"
	@echo "  $(GREEN)make create-venv$(NC)           Create a virtual environment and install requirements."
	@echo "  $(GREEN)make compile-requirements$(NC)  Compile requirements."
	@echo "  $(GREEN)make sync-requirements$(NC)     Sync requirements."
	@echo "  $(GREEN)make tox$(NC)                   Run tests with tox."
	@echo "  $(GREEN)make lint$(NC)                  Run all linters (black, isort, ruff)."
	@echo "  $(GREEN)make help$(NC)                  Show this help message."
	@echo "$(SEPARATOR)"

make run-lexer-docker:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Creating docker to run lexer script...$(NC)"
	@echo "$(SEPARATOR)"
	docker compose  -f docker_lexer/docker-compose-lexer.yml up

make run-parser-docker:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Creating docker to run parser script...$(NC)"
	@echo "$(SEPARATOR)"
	docker compose  -f docker-compose-parser.yml up

create-venv:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Creating virtual environment...$(NC)"
	@echo "$(SEPARATOR)"
	python3 -m venv .venv
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Activating virtual environment...$(NC)"
	@echo "$(SEPARATOR)"
	source .venv/bin/activate && \
		echo "$(PURPLE)Python version:$(NC)" && python --version && \
		echo "$(PURPLE)Upgrading pip...$(NC)" && pip install --upgrade pip && \
		echo "$(PURPLE)Installing pip-tools...$(NC)" && pip install pip-tools && \
		echo "$(PURPLE)Syncing requirements...$(NC)" && pip-sync requirements/requirements.txt

compile-requirements:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Compiling requirements...$(NC)"
	@echo "$(SEPARATOR)"
	pip-compile requirements/requirements.in -o requirements/requirements.txt

sync-requirements:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Syncing requirements...$(NC)"
	@echo "$(SEPARATOR)"
	pip-sync requirements/requirements.txt

# Lint and test

tox:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Running tests with tox...$(NC)"
	@echo "$(SEPARATOR)"
	tox

lint-black:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Linting with black...$(NC)"
	@echo "$(SEPARATOR)"
	black src

lint-isort:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Linting with isort...$(NC)"
	@echo "$(SEPARATOR)"
	isort src

lint-ruff:
	@echo "$(SEPARATOR)"
	@echo "$(PURPLE)Linting with ruff...$(NC)"
	@echo "$(SEPARATOR)"
	ruff src --fix

lint: lint-black lint-isort lint-ruff
