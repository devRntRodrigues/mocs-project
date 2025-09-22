.PHONY: fmt lint typecheck test ci

lint-format:
	uvx ruff format .

lint-fix:
	uvx ruff check --fix .
lint:
	uvx ruff check .

typecheck:
	uvx mypy .

test:
	uv run -m pytest -q

run:
	uv run main

ci: lint-format lint-fix typecheck test