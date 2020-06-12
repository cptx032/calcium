#!/usr/bin/env sh
isort **/*.py && black -l 79 **/*.py
mypy **/*.py --ignore-missing-imports
pyflakes **/*.py
PYTHONPATH=. python -m pytest tests/
