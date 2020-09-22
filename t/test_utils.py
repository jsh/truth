#!/usr/bin/env python3
"""Test utils module."""

import pytest

from utils import adjusted, excess, to_bytes, toggle_bit_in_byte


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


def test_excess() -> None:
    """Report excess correctly."""
    assert excess(16) == 0
    assert excess(18) == 2
    assert excess(14) == 6


def test_adjusted() -> None:
    """Report adjusted byte boundary correctly."""
    assert adjusted(16) == 16
    assert adjusted(18) == 16
    assert adjusted(14) == 8
