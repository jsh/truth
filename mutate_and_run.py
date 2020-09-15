#!/usr/bin/env python3
"""Drive the truth."""

import argparse
import sys

from parse_args import get_args
from zoon import Zoon


def mutate_and_run(args: argparse.Namespace) -> list:
    """Mutatate the wild type at each bit in a range and capture the results.
    :param args.Namespace args: All the args
    :return: list of results of all runs
    :rtype: list[tuple[int, str, str, str]]
    """
    zoon = Zoon(args.wild_type)
    start, end = args.start, args.end

    results = [None] * len(zoon)  # preallocate: thinking ahead to threadded version

    for bit in range(start, end):
        mutant = zoon.mutate(bit)
        results[bit] = mutant.run()
    assert None not in results[start:end], f"returncodes not set in {start}:{end}"
    # did we miss one?

    return results


def report(results: list, args: argparse.Namespace):
    """Report the results.
    :param list results: results to report
    :param args argparse.Namespace: contains args.start and args.end
    """
    for bit in range(args.start, args.end):
        result = results[bit]
        if args.verbose:
            print(f"mutant at bit {bit}: {result}")
        else:
            if result:
                print(f"{bit}\t{result[0]}")


def main(argv: list):
    """The big tent.
    :param list argv: All the args. sys.argv
    """

    args = get_args(
        "Brute-force survey of point mutants, every site in a span.", argv[1:]
    )
    print(args)
    results = mutate_and_run(args)
    report(results, args)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:
        print(f"Unexpected exception: {str(exc)}")
