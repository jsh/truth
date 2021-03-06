#!/usr/bin/env python3
"""Test parse_params() function."""

import logging
from pathlib import Path
import pytest

from paramparse import parse_params
from utils import pwhich


def test_defaults() -> None:
    """ParamParser defaults."""
    params = parse_params()
    assert params.loglevel == logging.ERROR
    assert params.wild_type == pwhich("true")
    assert not params.mutants
    assert not params.cmd_args
    assert not params.bit_range
    assert not params.bits_file


def test_verbose() -> None:
    """parse_param() understands --verbose."""
    params = parse_params(["--verbose"])
    assert params.loglevel == logging.INFO


def test_debug() -> None:
    """parse_param() understands --debug."""
    params = parse_params(["--debug"])
    assert params.loglevel == logging.DEBUG


def test_wild_type() -> None:
    """parse_param() understands --wild_type."""
    params = parse_params(["--wild_type=/etc/passwd"])
    assert params.wild_type == Path("/etc/passwd")


def test_mutants() -> None:
    """parse_param() understands --mutants."""
    params = parse_params(["--mutants=foobarmumble"])
    assert params.mutants == "foobarmumble"


def test_bit_range() -> None:
    """parse_param() understands --bit_range."""
    params = parse_params(["--bit_range=3:5"])
    assert params.bit_range == "3:5"


def test_bits_file() -> None:
    """parse_param() understands --bit_range."""
    params = parse_params(["--bits_file=/etc/passwd"])
    assert params.bits_file == "/etc/passwd"


def test_range_and_file() -> None:
    """parse_param() understands --bit_range and --bits_file are mutually exclusive.."""
    with pytest.raises(SystemExit):
        params = parse_params(["--bits_file=/etc/passwd", "--bit_range=1:2"])


def test_help() -> None:
    """Test help which throws a SystemExit."""
    # TODO: How do I do this?
