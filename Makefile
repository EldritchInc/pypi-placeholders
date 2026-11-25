.PHONY: install test lint format typecheck build check

install:
	python -m pip install -e azathoth-team -e eldritch-licensing build mypy pytest ruff

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff format .

typecheck:
	python -m mypy azathoth-team/src eldritch-licensing/src tests

build:
	python -m build --wheel --outdir dist azathoth-team
	python -m build --wheel --outdir dist eldritch-licensing

check:
	python -m ruff check .
	python -m ruff format --check .
	python -m mypy azathoth-team/src eldritch-licensing/src tests
	python -m pytest
