#!/usr/bin/env python3
"""Miscellaneous utility routines."""

import pathlib
import subprocess
from pathlib import Path


def to_bytes(binary_string: str) -> bytes:
    """Change a string, like "00000011" to a bytestring
    :param str binary_string: The string
    :returns: The bytestring
    :rtype: bytes
    """
    if len(binary_string) % 8 != 0:
        binary_string += "0" * (
            8 - len(binary_string) % 8
        )  # fill out to a multiple of 8

    assert set(binary_string) <= {"0", "1"}  # it really is a binary string
    assert len(binary_string) % 8 == 0  # it really is in 8-bit bytes
    size = len(binary_string) // 8
    binary_int = int(binary_string, 2)
    return binary_int.to_bytes(size, byteorder="big")


def toggle_bit_in_byte(offset: int, byte: int) -> int:
    """toggle a bit in a byte, from https://wiki.python.org/moin/BitManipulation
    :param int offset: the offest in the byte to toggle
    :param int byte: the byte
    :return: the new byte
    :rtype: int
    """
    assert 0 <= offset < 8
    assert 0 <= byte < 256
    mask = 1 << offset
    return byte ^ mask


def which(command: str) -> pathlib.Path:
    """An important default.
    :returns: Path to command
    :rtype: pathlib.Path
    """
    return Path(
        subprocess.check_output(
            f"which {command}", shell=True, universal_newlines=True
        ).strip()
    )


def valid_slice(start: int, stop: int, out_of_bounds: int) -> slice:
    """Valid slice of a Zoon.
    create a valid slice [start, stop)
    :param int start: the start of the slice
    :param int stop: the stop of the slice
    :param int out_of_bounds: upper limit for stop
    :returns: valid slice
    :rtype: slice
    """
    assert out_of_bounds > stop > start >= 0
    return slice(start, stop)