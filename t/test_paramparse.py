#!/usr/bin/env python3
"""Test param_parser() function."""

import logging
from pathlib import Path

from paramparse import ParamParser, Span
from utils import pwhich


def test_ParamParser_defaults() -> None:  # pylint:disable=invalid-name
    """ParamParser defaults."""
    params = ParamParser()
    assert params.loglevel == logging.WARNING
    assert not params.save
    assert params.wild_type == pwhich("true")
    assert not params.mutants
    assert not params.cmd_args
    assert params.size_in_bytes == Path(params.wild_type).stat().st_size
    assert params.size_in_bits == params.size_in_bytes * 8
    assert params.bits == Span(start=0, end=params.size_in_bits)
    assert params.bytes == Span(start=0, end=params.size_in_bytes)


def test_verbose() -> None:
    """ParamParser understands --verbose."""
    params = ParamParser(["--verbose"])
    assert params.loglevel == logging.INFO


def test_debug() -> None:
    """ParamParser understands --debug."""
    params = ParamParser(["--debug"])
    assert params.loglevel == logging.DEBUG


def test_save() -> None:
    """ParamParser understands --save."""
    params = ParamParser(["--save"])
    assert params.save


def test_wild_type() -> None:
    """ParamParser understands --wild_type."""
    params = ParamParser(["--wild_type=/etc/passwd"])
    assert params.wild_type == "/etc/passwd"


def test_mutants() -> None:
    """ParamParser understands --mutants."""
    params = ParamParser(["--mutants=foo"])
    assert params.mutants == "foo"


def test_bits() -> None:
    """ParamParser understands --bits."""
    params = ParamParser(["--bits=3:5"])
    assert params.bits == Span(start=3, end=5)


def test_bytes() -> None:
    """ParamParser understands --bytes."""
    params = ParamParser(["--bytes=6:9"])
    assert params.bytes == Span(start=6, end=9)


def test_help() -> None:
    """Test help which throws a SystemExit."""
    # TODO: How do I do this?
