.PHONY: create-venv compile-requirements sync-requirements tox lint help

# Default target
default: help

# Installation guide for development

create-venv:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Activating virtual environment..."
	source .venv/bin/activate && \
		echo "Python version:" && python --version && \
		echo "Upgrading pip..." && pip install --upgrade pip && \
		echo "Installing pip-tools..." && pip install pip-tools && \
		echo "Syncing requirements..." && pip-sync requirements/requirements.txt

compile-requirements:
	@echo "Compiling requirements..."
	pip-compile requirements/requirements.in -o requirements/requirements.txt

sync-requirements:
	@echo "Syncing requirements..."
	pip-sync requirements/requirements.txt

# Lint and test

tox:
	@echo "Running tests with tox..."
	tox

lint-black:
	@echo "Linting with black..."
	black src

lint-isort:
	@echo "Linting with isort..."
	isort src

lint-ruff:
	@echo "Linting with ruff..."
	ruff src --fix

lint: lint-black lint-isort lint-ruff

# Help

help:
	@echo "Available options:"
	@echo "  make create-venv           Create a virtual environment and install requirements."
	@echo "  make compile-requirements  Compile requirements."
	@echo "  make sync-requirements     Sync requirements."
	@echo "  make tox                   Run tests with tox."
	@echo "  make lint                  Run all linters (black, isort, ruff)."
	@echo "  make help                  Show this help message."
