#!/usr/bin/env python3
"""Test zoon module."""
# TODO: test a command with an arg.

from pathlib import Path

import pytest

from utils import to_bytes, which
from zoon import Zoon

TRUE = which("true")


def test_init_from_file():
    """__init__() works correctly from string"""
    zoon = Zoon(TRUE)
    assert "%r" % zoon == f"zoon.Zoon('{TRUE}', fromfile=True)"


def test_init_from_string():
    """__init__() works correctly from string."""
    zoon = Zoon("000011", fromfile=False)
    assert "%r" % zoon == "zoon.Zoon('000011', fromfile=False)"


def test_init_from_zoon():
    """__init__() works correctly from Zoon"""
    zoon = Zoon("00001100", fromfile=False)
    zoon2 = Zoon(zoon, fromfile=False)
    assert zoon2.byteseq == zoon.byteseq


def test_bad_string():
    """assert on attempt to create Zoon from non-binary string."""
    with pytest.raises(AssertionError):
        Zoon("abcdefgh", fromfile=False)


def test_bad_initializer():
    """assert on attempt to create Zoon from non-binary string."""
    with pytest.raises(TypeError):
        Zoon({}, fromfile=False)


def test_bad_file():
    """assert on attempt to create Zoon from non-file."""
    with pytest.raises(AssertionError):
        Zoon("mumblefrabitz")


def test_string_len():
    """len() works correctly on Zoon from string."""
    zoon = Zoon("00000011", fromfile=False)  # low bits set
    assert len(zoon) == 8
    zoon = Zoon("11000000", fromfile=False)  # high bits set
    assert len(zoon) == 8
    zoon = Zoon("11000000" * 100, fromfile=False)  # longer strings
    assert len(zoon) == 800
    zoon = Zoon("110000", fromfile=False)  # blank-pad
    assert len(zoon) == 8
    zoon = Zoon("0", fromfile=False)  # blank-pad really a lot
    assert len(zoon) == 8


def test_file_len():
    """len() works correctly on Zoon from file"""
    zoon = Zoon(TRUE)
    assert len(zoon) == Path(TRUE).stat().st_size * 8


def test_write_low(tmp_path):
    """Low bits set."""
    bit_string = "00000011"
    zoon = Zoon(bit_string, fromfile=False)
    bit_path = tmp_path / "bits"
    zoon.write(bit_path)
    assert bit_path.read_bytes() == to_bytes(bit_string)


def test_write_high(tmp_path):
    """High bits set."""
    bit_string = "11000000"
    zoon = Zoon(bit_string, fromfile=False)
    bit_path = tmp_path / "bits"
    zoon.write(bit_path)
    assert bit_path.read_bytes() == to_bytes(bit_string)


def test_write_missing(tmp_path):
    """0-pad on the right."""
    bit_string = "000011"
    zoon = Zoon(bit_string, fromfile=False)
    bit_path = tmp_path / "bits"
    zoon.write(bit_path)
    assert bit_path.read_bytes() == to_bytes(bit_string)


def test_mutate():
    """Mutate a bit in a Zoon"""
    zoon_0 = Zoon("00000000", fromfile=False)
    new_zoon = zoon_0.mutate(0)
    assert new_zoon.byteseq != zoon_0.byteseq
    zoon_1 = Zoon("00000001", fromfile=False)
    new_zoon = zoon_1.mutate(7)
    assert new_zoon.byteseq == zoon_0.byteseq


def test_run():
    """Run a zoon"""
    expected = (0, "success", "", "")
    zoon = Zoon(TRUE)
    assert zoon.run() == expected


def test_delete():
    """Deletes delete correctly."""
    one = "00000001"
    ten = "00001010"
    zoon_0 = Zoon(one + ten + one, fromfile=False)
    zoon_1 = Zoon(one * 2, fromfile=False)
    assert zoon_0.delete(8, 16).byteseq == zoon_1.byteseq
    assert zoon_0.delete(8, 17).byteseq == zoon_1.byteseq
    assert zoon_0.delete(10, 17).byteseq == zoon_1.byteseq
    assert zoon_0.delete(6, 17).byteseq != zoon_1.byteseq
    assert zoon_0.delete(17, 25).byteseq != zoon_1.byteseq
    assert zoon_0.delete(8, 9).byteseq != zoon_1.byteseq
    assert zoon_0.delete(0, 7).byteseq != zoon_1.byteseq
