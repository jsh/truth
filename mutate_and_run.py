#!/usr/bin/env python3
"""Drive the truth."""

import sys
from typing import Tuple

from parse_args import get_args
from zoon import Zoon

Result = Tuple[int, str, str, str]


def mutate_and_run(wild_type, start, end, verbose=False) -> None:
    """Mutatate the wild type at each bit in a range and capture the results.
    :param object wild_type: What to start with
    :param int start: where to start mutating
    :param int end: where to stop mutating
    :param args.Namespace args: All the args
    :param bool verbose: chatty or terse reporting?
    """
    zoon = Zoon(wild_type)

    for bit in range(start, end):
        mutant = zoon.mutate(bit)
        result = mutant.run()
        report(result, bit, verbose=verbose)


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
    mutate_and_run(args.wild_type, args.bits.start, args.bits.end, verbose=args.verbose)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:
        print(f"Unexpected exception: {str(exc)}")
