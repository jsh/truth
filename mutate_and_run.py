#!/usr/bin/env python3
"""Drive the truth."""

import atexit
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Tuple

from parse_args import get_args
from zoon import Zoon

Result = Tuple[int, str, str, str]


def survey_range(args) -> None:
    """Mutatate the wild type at each bit in a range and capture the results.
    :param args.Namespace args: All the args
    """
    zoon = Zoon(args.wild_type)
    cmd_args = args.cmd_args
    if args.mutant:  # name the file
        fs_path = Path(args.mutant)
    elif args.mutants:  # name the directory
        fs_path = Path(args.mutants)
    else:  # neither specified
        tempdir = tempfile.mkdtemp()  # use a temporary directory, then cleanup
        atexit.register(shutil.rmtree, tempdir)
        fs_path = Path(tempdir)
    for bit in range(args.bits.start, args.bits.end):
        result = zoon.mutate_and_run(position=bit, fs_path=fs_path, cmd_args=cmd_args)
        report(result, bit, verbose=args.verbose)


def report(result: Result, bit, verbose=False) -> None:
    """Report the results.
    :param list results: results to report
    :param int bit: mutated bit
    :param bool verbose: chatty or terse?
    """
    if verbose:
        print(f"mutant at bit {bit}: {result}")
    else:
        if result:
            print(f"{bit}\t{result[0]}")


def main(argv: list) -> None:
    """The big tent.
    :param list argv: All the args. sys.argv
    """

    args = get_args(
        "Brute-force survey of point mutants, every site in a span.", argv[1:]
    )
    if args.verbose:
        print(args, file=sys.stderr)
    survey_range(args)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:  # TODO: make more precise?
        print(f"Unexpected exception: {str(exc)}")
