#!/usr/bin/env python3
"""Test utils module."""
# TODO: fix mypy/pytest in a better way

import os
import sys

import pytest  # type: ignore

from utils import parsed_span, to_bytes, toggle_bit_in_byte, which


def test_which() -> None:
    """executing which() succeeds"""
    truepath = which("true")
    assert os.system(truepath) == 0


def test_to_bytes_low() -> None:
    """to_bytes() works with low bits set."""
    s = "00000011"
    assert to_bytes(s) == b"\x03"


def test_to_bytes_high() -> None:
    """to_bytes() works with high bits set."""
    s = "11000000"
    assert to_bytes(s) == b"\xc0"


def test_to_bytes_missing() -> None:
    """to_bytes() zero-pads on the right when necessary."""
    # 0-pad on the right
    s = "000011"
    assert to_bytes(s) == b"\x0c"


def test_to_bytes_badstring() -> None:
    """to_bytes() asserts on non-binary strings."""
    s = "abcde"
    with pytest.raises(AssertionError):
        assert to_bytes(s)


def test_toggle_bit_in_int() -> None:
    """toggle_bit_in_byte() flips the required bit."""
    assert toggle_bit_in_byte(0, 1) == 0
    assert toggle_bit_in_byte(0, 0) == 1
    assert toggle_bit_in_byte(1, 0) == 2
    assert toggle_bit_in_byte(2, 0) == 4
    assert toggle_bit_in_byte(3, 0) == 8
    assert toggle_bit_in_byte(4, 0) == 16
    assert toggle_bit_in_byte(5, 0) == 32
    assert toggle_bit_in_byte(6, 0) == 64
    assert toggle_bit_in_byte(7, 0) == 128
    with pytest.raises(AssertionError):
        toggle_bit_in_byte(8, 0)
    with pytest.raises(AssertionError):
        toggle_bit_in_byte(0, 256)


def test_parsed_span() -> None:
    """parsed_span handles all five span types"""
    assert (0, sys.maxsize) == parsed_span("")
    assert (69, 70) == parsed_span("69")
    assert (6, 9) == parsed_span("6:9")
    assert (69, sys.maxsize) == parsed_span("69:")
    assert (0, 69) == parsed_span(":69")
    assert (0, sys.maxsize) == parsed_span(":")
    # TODO: need a mock to set args.size

    with pytest.raises(TypeError):
        parsed_span("xxx")
