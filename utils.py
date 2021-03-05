#!/usr/bin/env pypy3
"""Miscellaneous utility routines."""

import shutil
import sys
from pathlib import Path


def make_range(indices: str = ":", upper_fence: int = sys.maxsize):
    """Make a range from a colon-separated string of ints."""
    pieces = [int(index) if index else None for index in indices.split(":")]
    if not pieces[0]:
        pieces[0] = 0
    if not pieces[-1]:
        pieces[-1] = upper_fence
    if len(pieces) == 1:
        return range(pieces[0], pieces[0] + 1)  # type: ignore
    return range(*pieces)  # type: ignore


def pwhich(command: str) -> Path:
    """Path to given command.

    shutil.which only returns a string.
    :returns: Path to command
    :rtype: pathlib.Path
    """
    path_str = shutil.which(command)
    assert path_str, f"{command} not found"
    return Path(path_str)


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
