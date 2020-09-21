#!/usr/bin/env python3
"""Drive the truth."""

import argparse
import sys
from typing import List, Tuple

from parse_args import get_args
from utils import adjusted
from zoon import Zoon


def delete_range_and_run(args: argparse.Namespace) -> List[Tuple[int, str, str, str]]:
    """Delete the chunk for the specified range, and run it.
    :param args.Namespace args: All the args
    :return: the results of the run
    :rtype: list[tuple[int, str, str, str]]
    """

    zoon = Zoon(args.wild_type)
    start, end = args.start, args.end
    start_byte = start // 8
    end_byte = end // 8 + 1
    # results = []
    # row = [None] * end_byte
    # for column in range(end_byte):
    #     results.append([None] * end_byte) # results starting at start_byte
    for deletion_start_byte in range(start_byte, end_byte - 1):
        for deletion_end_byte in range(deletion_start_byte + 1, end_byte):
            mutant = zoon.delete(deletion_start_byte * 8, deletion_end_byte * 8)
            result = mutant.run()
            #        results[deletion_start_byte][deletion_end_byte] = result
            report_now(result, args, deletion_start_byte, deletion_end_byte)

    # return results


def report_now(result: tuple, args, deletion_start_byte: int, deletion_end_byte: int):
    """Report the result.
    :param tuple results: results to report
    :param int deletion_start_byte: lower bound (included)
    :param int deletion_end_byte: upper bound (not included)
    """
    if args.verbose:
        print(f"deletion of {deletion_start_byte*8}:{deletion_end_byte*8}: {result}")
    else:
        if result:
            print(f"{deletion_start_byte*8}:{deletion_end_byte*8}\t{result[0]}")


def report(results: list, args: argparse.Namespace):
    """Report the results.
    :param list results: results to report
    :param args argparse.Namespace: contains args.start and args.end
    """
    start_byte = args.start // 8
    end_byte = (args.end // 8) + 1
    print(start_byte, end_byte)
    for deletion_start_byte in range(start_byte, end_byte - 1):
        for deletion_end_byte in range(deletion_start_byte + 1, end_byte):
            result = results[deletion_start_byte][deletion_end_byte]
            if args.verbose:
                print(
                    f"deletion of {deletion_start_byte*8}:{deletion_end_byte*8}: {result}"
                )
            else:
                if result:
                    print(f"{deletion_start_byte*8}:{deletion_end_byte*8}\t{result[0]}")


def main(argv: list):
    """The big tent.
    :param list argv: All the args. sys.argv
    """

    args = get_args("Delete a chunk and run.", argv[1:])
    args.start = adjusted(args.start)
    args.end = adjusted(args.end)
    print(args)
    delete_range_and_run(args)
    # results = delete_range_and_run(args)
    # report(results, args)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:
        print(f"Unexpected exception: {str(exc)}")
