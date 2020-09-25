#!/usr/bin/env python3
"""Miscellaneous utility routines."""

import collections
import pathlib
import re
import subprocess
import sys
from pathlib import Path

Span = collections.namedtuple("Span", "start end")


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


def excess(bit: int) -> int:
    """how far beyond the byte boundary is bit?
    :param int bit: the bit number
    :return: the excess
    :rtype: int
    """
    return bit % 8


def adjusted(bit: int) -> int:
    """how far beyond the byte boundary is bit?
    :param int bit: the bit number
    :return: bit shifted down to byte boundary
    :rtype: int
    """
    return bit - excess(bit)


def parsed_span(span: str) -> Span:
    """parse a span
    :param str bit: range specified
    :returns: beginning and end of span
    :rtype: tuple(int, int)
    """

    if not span:
        span = "0:"  # the entire sequence
    elif re.fullmatch(r"-?\d+", span):
        return Span(start=int(span), end=int(span) + 1)
    span_pat = r"(-?\d*):(-?\d*)"
    match = re.fullmatch(span_pat, span)
    if match:
        # pull apart "left:right", turn into start and end of range
        left = match.group(1)
        if not left:
            left = "0"
        start = int(left)
        right = match.group(2)
        end = int(right) if right else sys.maxsize
        return Span(start=start, end=end)
    raise TypeError("--bit argument must be a colon-separated range or a single int")
