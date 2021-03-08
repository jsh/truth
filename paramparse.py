#!/usr/bin/env pypy3
"""Get parameter values from cmdline, config files, and defaults."""


# TODO: typing for params, return values of functions
# TODO: make naming, calling conventions more parallel with other parsers: paramparse.ParamParser()
# pylint:disable=dangerous-default-value

import argparse
import collections
import configparser
import logging
from pathlib import Path

from utils import pwhich

APP_NAME = "truth"
RC_NAME = f"{APP_NAME}rc"
SYSTEM_CONFIG = f"/etc/{RC_NAME}"
GLOBAL_CONFIG = str(Path.home() / f".{RC_NAME}")
LOCAL_CONFIG = f".configs/{RC_NAME}"


def config_parser(configfiles):
    """Parse a configfile and return a named tuple of its contents."""
    # TODO: handle bits, cmd_args, mutants

    config = configparser.ConfigParser()
    config.read(configfiles)
    wild_type = config.get("core", "wild_type", fallback=pwhich("true"))

    Configs = collections.namedtuple("Configs", "wild_type")
    configs = Configs(wild_type=wild_type)
    return configs


def parse_params(args=None) -> argparse.Namespace:
    """Get the params
       Precedence is defaults < config files < cmdline

    When this finishes we return a Namespace that has these attributes
      - loglevel: how much info to log
      - mutants: directory for mutants
      - cmd_args: command arguments
      - bits: bit range
    """
    # TODO: update doc string

    parser = argparse.ArgumentParser(
        description="Brute-force survey of point mutants, every site in a span."
    )
    config_files = [SYSTEM_CONFIG, GLOBAL_CONFIG, LOCAL_CONFIG]
    defaults = config_parser(config_files)
    parser.add_argument(
        "-d",
        "--debug",
        help="Print DEBUG, INFO, WARNING, ERROR, CRITICAL",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.ERROR,
    )
    parser.add_argument(
        "-i",
        "--info",
        "--verbose",
        help="Print a lot: INFO, WARNING, ERROR, CRITICAL",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.ERROR,  # WARNING, ERROR, CRITICAL
    )
    parser.add_argument(
        "--wild_type",
        "--wt",
        default=defaults.wild_type,
        help="un-mutated executable (default: %(default)s)",
    )
    parser.add_argument(
        "--mutants", help="directory to store mutants"
    )  # TODO: should this default to "mutants"?
    parser.add_argument(
        "--cmd_args", help="args for the executable(s)"
    )  # TODO: should this default to ""?

    mutants = parser.add_mutually_exclusive_group()
    mutants.add_argument(
        "--bit_range",
        "--bits",
        "--bit",
        "-r",
        "-b",
        help="bit or range of bits of interest",
    )
    mutants.add_argument(
        "--bit_file", "--file", "-f", help="file containing bit(s) of interest"
    )

    if args is None:
        args = []
    params = parser.parse_args(args)
    # set up logging
    logging.basicConfig(level=params.loglevel, format="%(message)s")
    logging.debug(params)

    # attribute validatation
    params.wild_type = Path(params.wild_type)  # convert to a path
    assert params.wild_type.is_file(), f"No file {params.wild_type}"

    return params
