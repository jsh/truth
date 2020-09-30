#!/usr/bin/env python3
"""Argument handling."""

import argparse
import collections
import sys
from pathlib import Path
from typing import List, Optional

from utils import parsed_span, which

Span = collections.namedtuple("Span", "start end")


def get_args(
    description: str = None, args: Optional[List] = None
) -> argparse.Namespace:
    """Parse the args
    :param str description: description message for executable
    :param list or None args: the argument list to parse
    :returns: the args, massaged and sanity-checked
    :rtype: argparse.Namespace

    When this finishes we return a Namespace that has these attributes
      - verbose: how chatty to be (Bool)
      - wild_type: path to executable being considered (e.g., "/usr/bin/true")
      - bit_size: size of wild_type, in bits (int)
      - byte_size: size of wild_type, in bytes (int)
      - bits: bit-range of interest (Span)
      - bytes: byte-range of interest (Span)
      This is a little redundant, but it's convenient and simplifies other code.
    """

    parser = argparse.ArgumentParser(description=description)
    bits_or_bytes = parser.add_mutually_exclusive_group()
    bits_or_bytes.add_argument("--bits", help="bit(s) of interest", type=parsed_span)
    bits_or_bytes.add_argument("--bytes", help="bytes(s) of interest", type=parsed_span)
    parser.add_argument(
        "--wild_type",
        default=which("true"),
        help="un-mutated executable (default: %(default)s)",
    )
    parser.add_argument("--verbose", help="be extra chatty", action="store_true")
    parser.add_argument('--mutant', type=argparse.FileType("wb", bufsize=0), default="bin/mutant")
    assert description, "executable description required"
    if args is None:
        args = []

    parsed_args = parser.parse_args(args)
    if parsed_args.verbose:
        print(parsed_args, file=sys.stderr)

    # attribute validatation and enhancement
    # TODO: I could do file work with type=, too.
    assert Path(parsed_args.wild_type).is_file(), f"No file {parsed_args.wild_type}"

    # sizes
    parsed_args.size_in_bytes = Path(parsed_args.wild_type).stat().st_size
    parsed_args.size_in_bits = parsed_args.size_in_bytes * 8

    # bit- and byte-ranges
    # Note that parse_args() prevents both bits and bytes from being set
    if parsed_args.bits:
        bits_start, bits_end = parsed_args.bits
        bits_end = min(bits_end, parsed_args.size_in_bits)
        bytes_start = bits_start // 8
        bytes_end = (bits_end // 8) + 1
    elif parsed_args.bytes:
        bytes_start, bytes_end = parsed_args.bytes
        bytes_end = min(bytes_end, parsed_args.size_in_bytes)
        bits_start = bytes_start * 8
        bits_end = (bytes_end) * 8
    else:  # specifying neither means "the whole Zoon"
        bits_start, bits_end = 0, parsed_args.size_in_bits
        bytes_start, bytes_end = 0, parsed_args.size_in_bytes

    parsed_args.bits = Span(bits_start, bits_end)
    parsed_args.bytes = Span(bytes_start, bytes_end)

    return parsed_args
