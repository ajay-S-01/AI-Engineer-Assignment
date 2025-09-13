.PHONY: help install install-dev test test-cov lint format clean run docs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	pip install -e .

install-dev: ## Install the package with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src --cov-report=html --cov-report=term-missing

test-unit: ## Run unit tests only
	pytest -m unit

test-integration: ## Run integration tests only
	pytest -m integration

lint: ## Run linting
	flake8 src tests
	mypy src

format: ## Format code
	black src tests
	isort src tests

format-check: ## Check code formatting
	black --check src tests
	isort --check-only src tests

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

run: ## Run the Streamlit app
	streamlit run src/app.py

docs: ## Generate documentation
	@echo "Documentation is available in the docs/ directory"

setup: install-dev ## Set up development environment
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then cp env.example .env; echo "Created .env file from template"; fi
	@echo "Please edit .env file with your API keys"

check: format-check lint test ## Run all quality checks

ci: ## Run CI pipeline
	pytest --cov=src --cov-report=xml
	black --check src tests
	isort --check-only src tests
	flake8 src tests
	mypy src
