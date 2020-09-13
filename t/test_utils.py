#!/usr/bin/env python3
"""Test utils module."""

import pytest

try:
    from utils import to_bytes, toggle_bit_in_byte
except ImportError:
    import sys

    sys.path.append(".")
    from utils import to_bytes, toggle_bit_in_byte


def test_to_bytes_low():
    """to_bytes() works with low bits set."""
    s = "00000011"
    assert to_bytes(s) == b"\x03"


def test_to_bytes_high():
    """to_bytes() works with high bits set."""
    s = "11000000"
    assert to_bytes(s) == b"\xc0"


def test_to_bytes_missing():
    """to_bytes() zero-pads on the right when necessary."""
    # 0-pad on the right
    s = "000011"
    assert to_bytes(s) == b"\x0c"


def test_to_bytes_badstring():
    """to_bytes() asserts on non-binary strings."""
    s = "abcde"
    with pytest.raises(AssertionError):
        assert to_bytes(s)


def test_toggle_bit_in_int():
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
