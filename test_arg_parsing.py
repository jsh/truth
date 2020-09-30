#!/usr/bin/env python3
"""Drive the truth."""

import sys
from typing import Tuple
from pathlib import Path

from parse_args import get_args

Result = Tuple[int, str, str, str]


def main(argv: list) -> None:
    """The big tent.
    :param list argv: All the args. sys.argv
    """

    args = get_args(
        "Brute-force survey of point mutants, every site in a span.", argv[1:]
    )
    if args.verbose:
        print(args, file=sys.stderr)
    args.mutant.write(b"hello\n")
    print(Path("bin/mutant").stat().st_size)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:
        print(f"Unexpected exception: {str(exc)}")
