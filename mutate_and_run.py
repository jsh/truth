#!/usr/bin/env pypy3
"""Drive the truth."""

import atexit
import logging
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Tuple

from paramparse import ParamParser
from utils import make_range
from zoon import Zoon

RunResult = Tuple[int, str, str, str]


def survey_range(params) -> None:
    """Mutatate the wild type at each bit in a range and capture the results.
    :param args.Namespace params: All the args
    """
    zoon = Zoon(params.wild_type)
    cmd_args = params.cmd_args
    if params.mutants:  # name the directory
        dir_path = Path(params.mutants)
        dir_path.mkdir(parents=True, exist_ok=True)
    else:  # neither specified
        tempdir = tempfile.mkdtemp()  # use a temporary directory, then cleanup
        atexit.register(shutil.rmtree, tempdir)
        dir_path = Path(tempdir)
    for bit in make_range(params.bits, params.wild_type.stat().st_size):
        result = zoon.mutate_and_run(position=bit, dir_path=dir_path, cmd_args=cmd_args)
        if params.loglevel > logging.WARNING:
            print(f"{bit}\t{result[0]}")
        logging.warning("mutant at bit %d: %s", bit, result)
        if not params.mutants:
            (dir_path / str(bit)).unlink()  # cleanliness is next to Godliness


def main(argv: list) -> None:
    """The big tent.
    :param list argv: All the args. sys.argv
    """

    parser = ParamParser()
    params = parser.parse_params(argv[1:])
    survey_range(params)


if __name__ == "__main__":
    main(sys.argv)
