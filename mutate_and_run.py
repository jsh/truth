#!/usr/bin/env python3
"""Drive the truth."""

import atexit
import sys
from pathlib import Path
import shutil
import tempfile
from typing import Tuple

from parse_args import get_args
from zoon import Zoon

Result = Tuple[int, str, str, str]


def mutate_and_run(args) -> None:
    """Mutatate the wild type at each bit in a range and capture the results.
    :param args.Namespace args: All the args
    """
    zoon = Zoon(args.wild_type)
    if args.mutant:                  # name the file
        where = Path(args.mutant)
    elif args.mutants:              # name the directory
        where = Path(args.mutants)
    else:   # neither specified
        tempdir= tempfile.mkdtemp()   # use a temporary directory, then cleanup
        atexit.register(shutil.rmtree, tempdir)
        where = Path(tempdir)
    for bit in range(args.bits.start, args.bits.end):
        mutant = zoon.mutate(bit)
        result = mutant.run(where)
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
    mutate_and_run(args)


if __name__ == "__main__":
    main(sys.argv)
    # try:
    #     main(sys.argv)
    # except Exception as exc:
    #     print(f"Unexpected exception: {str(exc)}")
