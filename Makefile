# The usual

SOURCES := $(wildcard *.py)
TESTS := $(wildcard t/*.py)

all: lint test

lint: bandit black mypy pylint pylama

bandit:
	bandit -q .

black: isort
	black -q ${SOURCES} ${TESTS}

clean:
	git clean -dfx --exclude=bin --exclude=problems --exclude=results

coverage:
	- pytest -q --cov --cov-report=html
	open htmlcov/index.html

fixme:
	pylint -rn ${SOURCES} ${TESTS} | sort -t: -k2 -n -r

isort:
	isort ${SOURCES} ${TESTS}

mypy:
	mypy ${PWD}

pylama:
	pylama -o .config/pylama ${SOURCES} ${TESTS}

pylint:
	pylint --disable=fixme,broad-except -rn ${SOURCES} ${TESTS} | sort -t: -k2 -n -r

requirements.txt: ${SOURCES} ${TESTS}
	pip freeze > requirements.txt

test:
	pytest


.PHONY: all bandit black clean fixme lint mypy pylint pylama isort test
