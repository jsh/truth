#!/usr/bin/env python3
"""Test parse_args module.
Modelled on https://bit.ly/35u38gV
"""

import sys

from parse_args import parse_args


def test_verbose():
    """parse_args understands --verbose"""
    parser = parse_args(["--verbose"])
    assert parser.verbose


def test_capsys(capsys):
    """Sample capsys.
    From https://docs.pytest.org/en/stable/capture.html
    """
    print("hello")
    sys.stderr.write("world\n")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
    assert captured.err == "world\n"
    print("next")
    captured = capsys.readouterr()
    assert captured.out == "next\n"
