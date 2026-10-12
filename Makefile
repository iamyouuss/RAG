install:
	uv sync

run:
	uv run python3 main.py

debug:
	uv run python3 -m pdb main.py

lint:
	flake8 . /src
	mypy .  /src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src/ main.py
	uv run mypy --strict src/ main.py
