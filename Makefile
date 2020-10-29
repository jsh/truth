# The usual

ALL_PYTHON=$(wildcard *.py */*.py)
PYTHON_PROBLEMS = $(wildcard problems/*.py)
SOURCES=$(filter-out ${PYTHON_PROBLEMS}, ${ALL_PYTHON})

all: lint test

lint: black mypy pylint pylama

black: isort
	black -q ${SOURCES}

clean:
	git clean -dfx --exclude=bin --exclude=problems --exclude=results

coverage:
	- pytest --cov --cov-report=html -v . t
	open htmlcov/index.html

fixme:
	pylint -rn ${SOURCES} | sort -t: -k2 -n -r

isort:
	isort ${SOURCES}

mypy:
	mypy ${PWD}

pylama:
	pylama -o .config/pylama ${SOURCES}

pylint:
	pylint --disable=fixme,broad-except -rn ${SOURCES} | sort -t: -k2 -n -r

test:
	pytest -v . t


.PHONY: all black clean fixme lint mypy pylint pylama isort test
