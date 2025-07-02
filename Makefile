.PHONY: help install dev-install format lint test clean release-patch release-minor release-major

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

dev-install: ## Install development dependencies
	pip install -e .[dev]
	pre-commit install

format: ## Format code with Black and isort
	black .
	isort .

lint: ## Run linting checks
	flake8 .
	bandit -r . -f json -o bandit-report.json || true

test: ## Run tests (placeholder)
	@echo "Tests not implemented yet"

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

release-patch: ## Create a patch release
	python scripts/release.py patch

release-minor: ## Create a minor release
	python scripts/release.py minor

release-major: ## Create a major release
	python scripts/release.py major

check: ## Run all checks (format, lint, test)
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test

pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

setup: ## Initial setup for development
	$(MAKE) dev-install
	$(MAKE) format
	@echo "Setup complete! You can now start developing."
