#!/usr/bin/env python3
"""Test zoon module."""
# TODO: test a command with an arg.
# TODO: fix mypy/pytest in a better way

from pathlib import Path

import pytest  # type: ignore

from utils import to_bytes, which
from zoon import Zoon

TRUE = which("true")


def test_init_from_file() -> None:
    """__init__() works correctly from string"""
    zoon = Zoon(TRUE)
    assert "%r" % zoon == f"zoon.Zoon('{TRUE}', fromfile=True)"


def test_init_from_string() -> None:
    """__init__() works correctly from string."""
    zoon = Zoon("000011", fromfile=False)
    assert "%r" % zoon == "zoon.Zoon('000011', fromfile=False)"


def test_init_from_zoon() -> None:
    """__init__() works correctly from Zoon"""
    zoon = Zoon("00001100", fromfile=False)
    zoon2 = Zoon(zoon, fromfile=False)
    assert zoon2.byteseq == zoon.byteseq


def test_bad_string() -> None:
    """assert on attempt to create Zoon from non-binary string."""
    with pytest.raises(AssertionError):
        Zoon("abcdefgh", fromfile=False)


def test_bad_initializer() -> None:
    """assert on attempt to create Zoon from non-binary string."""
    with pytest.raises(TypeError):
        Zoon({}, fromfile=False)


def test_bad_file() -> None:
    """assert on attempt to create Zoon from non-file."""
    with pytest.raises(AssertionError):
        Zoon("mumblefrabitz")


def test_string_len() -> None:
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


def test_file_len() -> None:
    """len() works correctly on Zoon from file"""
    zoon = Zoon(TRUE)
    assert len(zoon) == Path(TRUE).stat().st_size * 8


def test_write_low(tmp_path) -> None:
    """Low bits set."""
    bit_string = "00000011"
    zoon = Zoon(bit_string, fromfile=False)
    bit_path = tmp_path / "bits"
    zoon.write(bit_path)
    assert bit_path.read_bytes() == to_bytes(bit_string)


def test_write_high(tmp_path) -> None:
    """High bits set."""
    bit_string = "11000000"
    zoon = Zoon(bit_string, fromfile=False)
    bit_path = tmp_path / "bits"
    zoon.write(bit_path)
    assert bit_path.read_bytes() == to_bytes(bit_string)


def test_write_missing(tmp_path) -> None:
    """0-pad on the right."""
    bit_string = "000011"
    zoon = Zoon(bit_string, fromfile=False)
    bit_path = tmp_path / "bits"
    zoon.write(bit_path)
    assert bit_path.read_bytes() == to_bytes(bit_string)


def test_write_bad_dir() -> None:
    """Write to a non-existent path."""
    zoon = Zoon(TRUE)
    with pytest.raises(FileNotFoundError):
        zoon.write(Path("/u/jane/me/tarzan"))


def test_write_temp_file(tmp_path) -> None:
    """Write to a temporary file."""
    zoon = Zoon(TRUE)
    assert tmp_path.is_dir()
    assert len(list(tmp_path.iterdir())) == 0
    zoon.write(tmp_path)
    assert len(list(tmp_path.iterdir())) == 1


def test_mutate() -> None:
    """Mutate a bit in a Zoon"""
    zoon_0 = Zoon("00000000", fromfile=False)
    new_zoon = zoon_0.mutate(0)
    assert new_zoon.byteseq != zoon_0.byteseq
    zoon_1 = Zoon("00000001", fromfile=False)
    new_zoon = zoon_1.mutate(7)
    assert new_zoon.byteseq == zoon_0.byteseq


def test_run(tmp_path) -> None:
    """Run a zoon"""
    expected = (0, "success", "", "")
    zoon = Zoon(TRUE)
    assert zoon.run(tmp_path) == expected


def test_delete() -> None:
    """Deletes delete correctly."""
    one = "00000001"
    ten = "00001010"
    zoon_0 = Zoon(one + ten + one, fromfile=False)
    zoon_1 = Zoon(one * 2, fromfile=False)
    assert zoon_0.delete(1, 2).byteseq == zoon_1.byteseq
    assert zoon_0.delete(0, 1).byteseq != zoon_1.byteseq
    assert zoon_0.delete(2, 3).byteseq != zoon_1.byteseq
    assert zoon_0.delete(0, 2).byteseq != zoon_1.byteseq
    assert zoon_0.delete(0, 3).byteseq != zoon_1.byteseq

def test_mutate_and_run() -> None:
    """mutate_and_run does that"""
    zoon = Zoon(TRUE)
    result = zoon.mutate_and_run(0, Path("mutant"), "--help", 1)  # TODO: create in a tempdir with a fixture
    assert result[1] != "success"
