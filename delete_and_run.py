#!/usr/bin/env python3
"""Drive the truth."""

import argparse
import sys

from parse_args import get_args
from zoon import Zoon


def delete_range_and_run(args: argparse.Namespace) -> None:
    """Delete the chunk for the specified range, and run it.
    :param args.Namespace args: All the args
    :return: the results of the run
    :rtype: list[tuple[int, str, str, str]]
    """

    zoon = Zoon(args.wild_type)
    start, end = args.bytes.start, args.bytes.end
    for deletion_start in range(start, end - 1):
        for deletion_end in range(deletion_start + 1, end):
            mutant = zoon.delete(deletion_start, deletion_end)
            if mutant:
                result = mutant.run()
                report(result, args, deletion_start, deletion_end)


def report(result: tuple, args, deletion_start: int, deletion_end: int) -> None:
    """Report the result.
    :param tuple results: results to report
    :param int deletion_start: lower bound (included)
    :param int deletion_end: upper bound (not included)
    """
    if args.verbose:
        print(f"deletion of bytes {deletion_start}:{deletion_end}: {result}")
    else:
        if result:
            print(f"{deletion_start}:{deletion_end}\t{result[0]}")


def main(argv: list) -> None:
    """The big tent.
    :param list argv: All the args. sys.argv
    """

    args = get_args("Delete a chunk and run.", argv[1:])
    delete_range_and_run(args)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:
        print(f"Unexpected exception: {str(exc)}")
