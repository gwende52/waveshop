.PHONY: help test test-verbose test-cov lint clean

# Paths
SRC_DIR := src
PYTHON := poetry run python
PYTEST := poetry run pytest

help:
	@echo "Available targets:"
	@echo "  test               — run all unit tests (with .env.test)"
	@echo "  test-verbose       — run tests with verbose output"
	@echo "  test-cov           — run tests with coverage (HTML report)"
	@echo "  lint               — run ruff + mypy"
	@echo "  clean              — remove coverage, cache, pyc"

test:
	@echo "🔍 Running unit tests..."
	$(PYTEST) $(SRC_DIR) --tb=short -q

test-verbose:
	@echo "🔍 Running unit tests (verbose)..."
	$(PYTEST) $(SRC_DIR) -v --tb=long

test-cov:
	@echo "📊 Running tests with coverage..."
	$(PYTEST) $(SRC_DIR) --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html
	@echo "➡️  Report: file://$(shell pwd)/htmlcov/index.html"

lint:
	@echo "🧹 Running ruff and mypy..."
	poetry run ruff check $(SRC_DIR)
	poetry run ruff format --check $(SRC_DIR)
	poetry run mypy $(SRC_DIR)

clean:
	rm -rf htmlcov .pytest_cache .mypy_cache
	find $(SRC_DIR) -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find $(SRC_DIR) -type f -name "*.pyc" -delete 2>/dev/null || true