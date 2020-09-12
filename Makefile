# The usual

SOURCES=$(wildcard *.py t/*.py)

all: lint test

lint: black pylint pylama

black: isort
	black -q ${SOURCES}

fixme:
	pylint -rn ${SOURCES} | sort -t: -k2 -n -r

isort:
	isort ${SOURCES}

pylama:
	pylama ${SOURCES}

pylint:
	pylint --disable=fixme -rn ${SOURCES} | sort -t: -k2 -n -r

test:
	PYTHONPATH=${PWD} pytest


.PHONY: all black fixme lint pylint pylama isort test
