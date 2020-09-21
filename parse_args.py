#!/usr/bin/env python3
"""Argument handling."""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

from utils import which


def get_args(description: str, args: List = None) -> argparse.Namespace:
    """Parse the args
    :param str description: description message for executable
    :param list args: the argument list to parse
    :returns: the args, massaged and sanity-checked
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--bit", help="bit(s) of interest")
    parser.add_argument(
        "--wild_type", default=which("true"), help="un-mutated executable"
    )
    parser.add_argument("--verbose", help="be extra chatty", action="store_true")
    if args is None:
        args = []

    parsed_args = parser.parse_args(args)

    assert Path(parsed_args.wild_type).is_file(), f"No file {parsed_args.wild_type}"
    parsed_args.size = Path(parsed_args.wild_type).stat().st_size * 8
    # TODO: perhaps make the span a named tuple, "parsed.span"
    parsed_args.start, parsed_args.end = parse_span(parsed_args.bit)
    if parsed_args.end == sys.maxsize:
        parsed_args.end = parsed_args.size
    return parsed_args


def parse_span(bit: str) -> Tuple[int, int]:
    """parse a span
    :param str bit: range specified
    :returns: beginning and end of span
    :rtype: tuple(int, int)
    """
    span = r"(\d*):(\d*)"
    if not bit:
        bit = "0:"  # the entire sequence
    match = re.fullmatch(span, bit)
    if match:
        # pull apart "left:right", turn into start and end of range
        left = match.group(1)
        if not left:
            left = "0"
        start = int(left)
        right = match.group(2)
        end = int(right) if right else sys.maxsize
    elif re.fullmatch(r"\d*", bit):
        start, end = (int(bit), int(bit) + 1)
    else:
        raise TypeError(
            "--bit argument must be a colon-separated range or a single int"
        )
    return (start, end)
