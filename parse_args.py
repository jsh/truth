#!/usr/bin/env python3
"""Argument handling."""

import argparse
import atexit
import collections
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from utils import parsed_span, which

Span = collections.namedtuple("Span", "start end")


def bit_and_byte_ranges(parsed_args: argparse.Namespace) -> Tuple[Span, Span]:
    """
    :param argparse.Namespace parsed_args: parsed args
    :returns: bit- and byte-ranges
    :rtype: Tuple[Span, Span]
    Note that parse_args() prevents both bits and bytes from being set
    """
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


def output_paths(parsed_args: argparse.Namespace):
    """
    some damn string
    :param argparse.Namespace parsed_args: parsed args
    """
    if parsed_args.mutant:  # name file to keep it in a particular place
        basepath = Path(parsed_args.mutant)
        dirpath = basepath.parent
    elif parsed_args.mutants:  # random filename in named directory
        dirpath = Path(parsed_args.mutants)
        basepath = Path(tempfile.NamedTemporaryFile(dir=parsed_args.mutants).name)
    else:  # one or more temporary files in temporary directory
        dirpath = Path(tempfile.mkdtemp())
        atexit.register(shutil.rmtree, dirpath)  # cleanup on exit
        basepath = None
    return basepath, dirpath


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
    mutant_or_mutants = parser.add_mutually_exclusive_group()
    mutant_or_mutants.add_argument("--mutant", help="file to store mutant")
    mutant_or_mutants.add_argument("--mutants", help="directory to store mutants")
    assert description, "executable description required"
    if args is None:
        args = []

    parsed_args = parser.parse_args(args)
    if parsed_args.verbose:
        print(parsed_args, file=sys.stderr)

    # attribute validatation and enhancement
    assert Path(parsed_args.wild_type).is_file(), f"No file {parsed_args.wild_type}"

    # bits and bytes
    parsed_args.size_in_bytes = Path(parsed_args.wild_type).stat().st_size
    parsed_args.size_in_bits = parsed_args.size_in_bytes * 8
    parsed_args.bits, parsed_args.bytes = bit_and_byte_ranges(parsed_args)

    # mutant paths
    parsed_args.basepath, parsed_args.dirpath = output_paths(parsed_args)

    return parsed_args
