#!/usr/bin/env python3
"""Test parse_params() function."""

import logging
from pathlib import Path

from paramparse import ParamParser, Span
from utils import pwhich


def test_defaults() -> None:
    """ParamParser defaults."""
    parser = ParamParser()
    params = parser.parse_params()
    assert params.loglevel == logging.WARNING
    assert params.wild_type == pwhich("true")
    assert not params.mutants
    assert not params.cmd_args
    assert params.size_in_bytes == Path(params.wild_type).stat().st_size
    assert params.size_in_bits == params.size_in_bytes * 8
    assert params.bits == Span(start=0, end=params.size_in_bits)
    assert params.bytes == Span(start=0, end=params.size_in_bytes)


def test_verbose() -> None:
    """parse_param() understands --verbose."""
    parser = ParamParser()
    params = parser.parse_params(["--verbose"])
    assert params.loglevel == logging.INFO


def test_debug() -> None:
    """parse_param() understands --debug."""
    parser = ParamParser()
    params = parser.parse_params(["--debug"])
    assert params.loglevel == logging.DEBUG


def test_wild_type() -> None:
    """parse_param() understands --wild_type."""
    parser = ParamParser()
    params = parser.parse_params(["--wild_type=/etc/passwd"])
    assert params.wild_type == Path("/etc/passwd")


def test_mutants() -> None:
    """parse_param() understands --mutants."""
    parser = ParamParser()
    params = parser.parse_params(["--mutants=foo"])
    assert params.mutants == "foo"


def test_bits() -> None:
    """parse_param() understands --bits."""
    parser = ParamParser()
    params = parser.parse_params(["--bits=3:5"])
    assert params.bits == Span(start=3, end=5)


def test_bytes() -> None:
    """parse_param() understands --bytes."""
    parser = ParamParser()
    params = parser.parse_params(["--bytes=6:9"])
    assert params.bytes == Span(start=6, end=9)


def test_help() -> None:
    """Test help which throws a SystemExit."""
    # TODO: How do I do this?
