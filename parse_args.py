#!/usr/bin/env python3
"""Argument handling."""

import argparse
import collections
import logging
from pathlib import Path
from typing import List, Optional, Tuple

from utils import parsed_span, pwhich

Span = collections.namedtuple("Span", "start end")


def bit_and_byte_ranges(parsed_args: argparse.Namespace) -> Tuple[Span, Span]:
    """
    :param argparse.Namespace parsed_args: parsed args
    :returns: bit- and byte-ranges
    :rtype: Tuple[Span, Span]
    Note that parse_args() prevents both bits and bytes from being set
    """
    # TODO: fix negative range handling.
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

    return Span(bits_start, bits_end), Span(bytes_start, bytes_end)


def get_args(
    description: str = None, args: Optional[List] = None
) -> argparse.Namespace:
    """Parse the args
    :param str description: description message for executable
    :param list or None args: the argument list to parse
    :returns: the args, massaged and sanity-checked
    :rtype: argparse.Namespace

    When this finishes we return a Namespace that has these attributes
      - debug: print everything
      - verbose: print everything below debug
      - wild_type: path to executable being considered
        (e.g., "/usr/bin/true"). [Must exist.]
      - bit_size: size of wild_type, in bits (int)
      - byte_size: size of wild_type, in bytes (int)
      - bits: bit-range of interest (Span) [default: entire wild_type]
      - bytes: byte-range of interest (Span) [default: entire wild_type]
      - mutants: a directory for mutants (str) [default: mutants]
    """
    if args is None:
        args = []

    assert description, "executable description required"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-d",
        "--debug",
        help="Print DEBUG, INFO, WARNING, ERROR, CRITICAL",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-i",
        "-v",
        "--info",
        "--verbose",
        help="Print a lot: INFO, WARNING, ERROR, CRITICAL",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.WARNING,  # WARNING, ERROR, CRITICAL
    )

    parser.add_argument(
        "--wild_type",
        default=pwhich("true"),
        help="un-mutated executable (default: %(default)s)",
    )

    parser.add_argument("--mutants", help="directory to store mutants")
    parser.add_argument("--cmd_args", help="args for the executable(s)")

    bits_or_bytes = parser.add_mutually_exclusive_group()
    bits_or_bytes.add_argument("--bits", help="bit(s) of interest", type=parsed_span)
    bits_or_bytes.add_argument("--bytes", help="bytes(s) of interest", type=parsed_span)

    parsed_args = parser.parse_args(args)
    # set up logging
    logging.basicConfig(level=parsed_args.loglevel, format="%(message)s")
    logging.debug(parsed_args)

    # attribute validatation and enhancement
    assert Path(parsed_args.wild_type).is_file(), f"No file {parsed_args.wild_type}"

    # bits and bytes
    parsed_args.size_in_bytes = Path(parsed_args.wild_type).stat().st_size
    parsed_args.size_in_bits = parsed_args.size_in_bytes * 8
    parsed_args.bits, parsed_args.bytes = bit_and_byte_ranges(parsed_args)

    return parsed_args
