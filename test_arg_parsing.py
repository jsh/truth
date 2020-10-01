#!/usr/bin/env python3
"""Drive the truth."""

import sys
from pathlib import Path
import tempfile
from typing import Tuple

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
    print(args.mutants)
    if args.mutants:
        mutants_name = args.mutants
    else:
        mutants_name = tempfile.mkdtemp()

    mutant_name = tempfile.NamedTemporaryFile(dir=mutants_name).name
    print("dir = ", mutants_name, "type= ", type(mutants_name))
    print("file = ", mutant_name, "type = ", type(mutant_name))
    mutant_path = Path(mutant_name)
    mutant_path.write_bytes(b"hello\n")
    mutant_path.chmod(0o755)
    mutant2_name = tempfile.NamedTemporaryFile(dir=mutants_name).name
    print("file = ", mutant2_name, "type = ", type(mutant2_name))
    mutant2_path = Path(mutant2_name)
    mutant2_path.write_bytes(b"hello\n")

    print(mutant_path.stat().st_size)
    print(mutant2_path.stat().st_size)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:
        print(f"Unexpected exception: {str(exc)}")
