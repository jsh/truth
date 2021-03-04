# The usual

BANDIT_OPTIONS := -q -s B101,B603  # don't warn about asserts
NO_CLEAN := bin problems results
PIPENV_PACKAGES := bandit isort mypy pycodestyle pydocstyle pyflakes pylama pylama_pylint pytest pytest-cov
PYTEST_OPTIONS := -q --doctest-modules
SOURCES := $(wildcard *.py)
TESTS := $(wildcard t/*.py)

all: lint security test

bandit:
	bandit ${BANDIT_OPTIONS} ${SOURCES} ${TESTS}

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

lint: black pylama bandit mypy

mypy:
	mypy ${PWD}

pipenv_setup:   # run this once, during initialization
	pipenv install --dev
	pipenv install ${PIPENV_PACKAGES}
	pipenv shell

pylama:
	pylama -o .config/pylama ${SOURCES} ${TESTS}

pylint:
	pylint --rcfile=.config/pylint -rn ${SOURCES} ${TESTS} | sort -t: -k2 -n -r

pytest test:
	pytest ${PYTEST_OPTIONS}

security: bandit
	pipenv check

.PHONY: all bandit black coverage clean fixme isort lint mypy pipenv_setup pylama pylint pytest security test
