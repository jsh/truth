#!/usr/bin/env python3
"""Parse arguments testably.
Modelled on https://bit.ly/35u38gV
"""

import argparse
import sys


def parse_args(args):
    """The argument parser
    :param list[str] args:
    :returns: parsed args
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Parse some arguments")
    parser.add_argument("--verbose", help="be extra chatty", action="store_true")
    return parser.parse_args(args)


def main():
    """The big top."""
    args = parse_args(sys.argv[1:])
    if args.verbose:
        print("See? It worked.")


if __name__ == "__main__":
    main()
