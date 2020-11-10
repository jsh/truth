# The usual

NO_CLEAN := bin problems results
PYTEST_OPTIONS := -q --doctest-modules
PIPENV_PACKAGES := bandit isort mypy pycodestyle pydocstyle pyflakes pylama pylama_pylint pytest pytest-cov
SOURCES := $(wildcard *.py)
TESTS := $(wildcard t/*.py)

all: lint test requirements.txt

bandit:
	bandit -q -s B101 ${SOURCES}

black: isort
	black -q ${SOURCES} ${TESTS}

clean:
	git clean -dfx ${NO_CLEAN:%=--exclude %}

coverage:
	- pytest ${PYTEST_OPTIONS} --cov="." --cov-report=html
	open htmlcov/index.html

fixme:
	pylint -rn ${SOURCES} ${TESTS} | sort -t: -k2 -n -r

isort:
	isort ${SOURCES} ${TESTS}

lint: black pylama bandit

mypy:
	mypy ${PWD}

pipenv_setup:   # run this once, during initialization
	pipenv install --dev
	pipenv install ${PIPENV_PACKAGES}
	pipenv shell

pylama:
	pylama -o .config/pylama ${SOURCES} ${TESTS}

pylint:
	pylint --disable=fixme,broad-except -rn ${SOURCES} ${TESTS} | sort -t: -k2 -n -r

requirements.txt: ${SOURCES} ${TESTS}
	pip freeze > requirements.txt

test:
	pytest ${PYTEST_OPTIONS}

.PHONY: all bandit black coverage clean fixme isort lint mypy pipenv_setup pylama pylint test
