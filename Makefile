install:

run:

debug:

lint:
flake8 . /src
mypy .  /src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:

