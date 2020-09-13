#!/usr/bin/env python3
"""Test parse_args module.
Modeled on https://bit.ly/35u38gV
"""

import os
import sys

import pytest

try:
    from parse_args import get_args, parse_span, which
except ImportError:
    sys.path.append(".")
    from parse_args import get_args, parse_span, which


def test_which():
    """executing which() succeeds"""
    truepath = which("true")
    assert os.system(truepath) == 0


def test_get_args_defaults():
    """get_args defaults"""
    parser = get_args("Testing default wild_type")
    assert parser.wild_type == which("true")


def test_bit():
    """get_args understands --bit"""
    parser = get_args("Testing bit", ["--bit=69"])
    assert parser.start == 69


def test_wild_type():
    """get_args understands --wild_type"""
    falsepath = which("false")
    parser = get_args("Testing wild_type", [f"--wild_type={falsepath}"])
    assert parser.wild_type == f"{falsepath}"


def test_verbose():
    """get_args understands --verbose"""
    parser = get_args("Testing verbose", ["--verbose"])
    assert parser.verbose


def test_help():
    """test help which throws a SystemExit"""
    # TODO: How do I do this?


def test_parse_span():
    """parse_span handles all five span types"""
    assert (0, sys.maxsize) == parse_span("")
    assert (69, 70) == parse_span("69")
    assert (6, 9) == parse_span("6:9")
    assert (69, sys.maxsize) == parse_span("69:")
    assert (0, 69) == parse_span(":69")
    assert (0, sys.maxsize) == parse_span(":")
    # TODO: need a mock to set args.size

    with pytest.raises(TypeError):
        parse_span("xxx")
