#!/usr/bin/env python3
"""Drive the truth."""

import atexit
import logging
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Tuple

from paramparse import ParamParser
from zoon import Zoon

RunResult = Tuple[int, str, str, str]


def survey_range(args) -> None:
    """Mutatate the wild type at each bit in a range and capture the results.
    :param args.Namespace args: All the args
    """
    zoon = Zoon(args.wild_type)
    cmd_args = args.cmd_args
    if args.mutants:  # name the directory
        dir_path = Path(args.mutants)
        dir_path.mkdir(parents=True, exist_ok=True)
    else:  # neither specified
        tempdir = tempfile.mkdtemp()  # use a temporary directory, then cleanup
        atexit.register(shutil.rmtree, tempdir)
        dir_path = Path(tempdir)
    for bit in range(args.bits.start, args.bits.end):
        result = zoon.mutate_and_run(position=bit, dir_path=dir_path, cmd_args=cmd_args)
        report(result, bit)
        if not args.save:
            (dir_path / str(bit)).unlink()  # cleanliness is next to Godliness


def report(result: RunResult, bit) -> None:
    """Report the results.
    :param list results: results to report
    :param int bit: mutated bit
    """
    logging.info("mutant at bit %d: %s", bit, result)
    if result:
        print(f"{bit}\t{result[0]}")


def main(argv: list) -> None:
    """The big tent.
    :param list argv: All the args. sys.argv
    """

    params = ParamParser(argv[1:])
    survey_range(params)


if __name__ == "__main__":
    main(sys.argv)
