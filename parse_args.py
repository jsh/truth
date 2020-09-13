#!/usr/bin/env python3
"""Argument handling."""

import argparse
import re
import sys
from pathlib import Path


def truth():
    """An important default.
    :returns: absoute Path to truth
    :rtype: pathlib.Path
    """
    reltruth = Path("bin/true")
    abstruth = "/" / reltruth
    if not abstruth.is_file():
        abstruth = "/usr" / reltruth
    assert abstruth.is_file()
    return abstruth


def get_args(description, args=None):
    """Parse the args
    :param str description: description message for executable
    :returns: the args, massaged and sanity-checked
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--bit", help="bit(s) of interest")
    parser.add_argument("--wild_type", default=truth(), help="un-mutated executable")
    parser.add_argument("--verbose", help="be extra chatty", action="store_true")

    args = parser.parse_args(args)

    assert Path(args.wild_type).is_file(), f"No file {args.wild_type}"
    args.size = Path(args.wild_type).stat().st_size * 8
    args.start, args.end = parse_span(args.bit)
    if args.end == sys.maxsize:
        args.end = args.size
    return args


def parse_span(bit):
    """parse a span
    :param str bit: range specified
    :returns: beginning and end of span
    :rtype: tuple(int, int)
    """
    span = r"(\d*):(\d*)"
    if not bit:
        bit = "0:"  # the entire sequence
    if re.fullmatch(span, bit):
        # pull apart start and end
        match = re.fullmatch(span, bit)
        start = match.group(1)
        if not start:
            start = "0"
        start = int(start)
        end = match.group(2)
        end = int(end) if end else sys.maxsize
    elif re.fullmatch(r"\d*", bit):
        start, end = (int(bit), int(bit) + 1)
    else:
        raise TypeError(
            "--bit argument must be a colon-separated range or a single int"
        )
    return (start, end)
