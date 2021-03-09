#!/usr/bin/env python3
"""Test utils module."""

import subprocess  # nosec
import sys

import pytest

from utils import make_range, pwhich, to_bytes, toggle_bit_in_byte


def test_pwhich() -> None:
    """Executing pwhich() succeeds."""
    truepath = pwhich("true")
    assert subprocess.run(str(truepath), check=True).returncode == 0  # nosec


def test_to_bytes_low() -> None:
    """to_bytes() works with low bits set."""
    bstr = "00000011"
    assert to_bytes(bstr) == b"\x03"


def test_to_bytes_high() -> None:
    """to_bytes() works with high bits set."""
    bstr = "11000000"
    assert to_bytes(bstr) == b"\xc0"


def test_to_bytes_missing() -> None:
    """to_bytes() zero-pads on the right when necessary."""
    # 0-pad on the right
    bstr = "000011"
    assert to_bytes(bstr) == b"\x0c"


def test_to_bytes_badstring() -> None:
    """to_bytes() asserts on non-binary strings."""
    bad_bstr = "abcde"
    with pytest.raises(AssertionError):
        assert to_bytes(bad_bstr)


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


def test_make_range() -> None:
    """make_range handles all five span types."""
    # upper_fence = sys.maxsize * 8   # pytest can't compare numbers this big.
    # assert range(0, upper_fence) == make_range()
    # assert range(69, sys.maxsize) == make_range("69:")
    assert range(69, 70) == make_range("69")
    assert range(6, 9) == make_range("6:9")
    assert range(0, 69) == make_range(":69")
    assert range(0, 5) == make_range(":", 5)
    assert range(2, 0, -1) == make_range("2:0:-1")
