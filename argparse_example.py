#!/usr/bin/env python3
"""Argument handling."""

import argparse
import sys
from typing import List, Optional
from utils import parsed_span, which


def get_args(
    description: str = None, args: Optional[List] = None
) -> argparse.Namespace:
    """Parse the args
    :param str description: description message for executable
    :param list or None args: the argument list to parse
    :returns: the args, massaged and sanity-checked
    :rtype: argparse.Namespace
    """

    # TODO: I can do a lot of argument validation with "type="

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
    # do some more arg manipulation and validation
    return parsed_args


if __name__ == "__main__":
    get_args(description="Description", args=sys.argv[1:])
