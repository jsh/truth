#!/usr/bin/env python3
"""Test parse_args module.
Modeled on https://bit.ly/35u38gV
"""

import pytest

from parse_args import get_args
from utils import which


def test_get_args_defaults() -> None:
    """get_args defaults"""
    parser = get_args("Testing default wild_type")
    assert parser.wild_type == which("true")


def test_bits() -> None:
    """get_args understands --bits"""
    parser = get_args("Testing bits", ["--bits=69"])
    assert parser.bits.start == 69


def test_bits_to_end() -> None:
    """get_args understands --bits"""
    parser = get_args("Testing bits", ["--bits=69"])
    assert parser.bits.start == 69


def test_bytes() -> None:
    """get_args understands --bytes"""
    parser = get_args("Testing bytes", ["--bytes=69"])
    assert parser.bytes.start == 69


def test_bytes_to_end() -> None:
    """get_args understands --bytes"""
    parser = get_args("Testing bytes", ["--bytes=69:"])
    assert parser.bytes.start == 69


def test_wild_type() -> None:
    """get_args understands --wild_type"""
    falsepath = which("false")
    parser = get_args("Testing wild_type", [f"--wild_type={falsepath}"])
    assert parser.wild_type == f"{falsepath}"


def test_verbose() -> None:
    """get_args understands --verbose"""
    parser = get_args("Testing verbose", ["--verbose"])
    assert parser.verbose


def test_argument_bits_and_bytes() -> None:
    """specifying both --bits and --bytes raises exception"""
    with pytest.raises(SystemExit):
        get_args("Testing illegal arg combo", ["--bytes=69:", "--bits=69:"])


def test_help() -> None:
    """test help which throws a SystemExit"""
    # TODO: How do I do this?
