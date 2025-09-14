.PHONY: help install install-dev test test-cov test-report test-unit test-integration lint format clean run docs setup check ci

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	pip install -e .

install-dev: ## Install the package with development dependencies
	pip install -e ".[dev]"

test: ## Run all tests
	pytest -v

test-cov: ## Run tests with coverage
	pytest -v --cov=src --cov-report=term-missing

test-report: ## Run tests and export results (JUnit XML)
	pytest -v --junitxml=reports/test-results.xml

test-unit: ## Run unit tests only
	pytest -m unit -v

test-integration: ## Run integration tests only
	pytest -m integration -v

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
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/
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
