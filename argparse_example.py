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
    assert description, "executable description required"
    if args is None:
        args = []

    parsed_args = parser.parse_args(args)
    print(parsed_args)

    # argument validatation and manipulation
    # TODO: I could do file work with type=, too.
    assert Path(parsed_args.wild_type).is_file(), f"No file {parsed_args.wild_type}"

    parsed_args.size = Path(parsed_args.wild_type).stat().st_size * 8

    assert (
        parsed_args.bit ^ parsed_args.byte
    ), "Specify either bits or bytes, but not both."
    if parsed_args.bits:
        bytes_start = parsed_args.bits.start // 8
        if parsed_args.bits.end == sys.maxsize:
            parsed_args.bits.end = parsed_args.size
        bytes_end = parsed_args.bits.end // 8
        parsed_args.bytes = Span(bytes_start, bytes_end)
    elif parsed_args.bytes:
        bits_start = parsed_args.bytes.start * 8
        if parsed_args.bytes.end == sys.maxsize:
            bits_end = parsed_args.size
        parsed_args.bytes.end = bits_end // 8
        parsed_args.bits = Span(bits_start, bits_end)

    return parsed_args


if __name__ == "__main__":
    get_args(description="Description", args=sys.argv[1:])
