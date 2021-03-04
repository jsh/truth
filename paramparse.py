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
from typing import Tuple

from utils import parsed_span, pwhich

APP_NAME = "truth"
RC_NAME = f"{APP_NAME}rc"
SYSTEM_CONFIG = f"/etc/{RC_NAME}"
GLOBAL_CONFIG = str(Path.home() / f".{RC_NAME}")
LOCAL_CONFIG = f".configs/{RC_NAME}"

Span = collections.namedtuple("Span", "start end")


def bit_and_byte_ranges(params: argparse.Namespace) -> Tuple[Span, Span]:
    """
    Note that ParamParser() prevents both bits and bytes from being set
    """
    # TODO: fix negative range handling.
    if params.bits:
        bits_start, bits_end = params.bits
        bits_end = min(bits_end, params.size_in_bits)
        bytes_start = bits_start // 8
        bytes_end = (bits_end // 8) + 1
    elif params.bytes:
        bytes_start, bytes_end = params.bytes
        bytes_end = min(bytes_end, params.size_in_bytes)
        bits_start = bytes_start * 8
        bits_end = (bytes_end) * 8
    else:  # specifying neither means "the whole Zoon"
        bits_start, bits_end = 0, params.size_in_bits
        bytes_start, bytes_end = 0, params.size_in_bytes

    return Span(bits_start, bits_end), Span(bytes_start, bytes_end)


def config_parser(configfiles):
    """Parse a configfile and return a named tuple of its contents."""
    # TODO: handle bits, bytes, cmd_args, mutants

    config = configparser.ConfigParser()
    config.read(configfiles)
    wild_type = config.get("core", "wild_type", fallback=pwhich("true"))

    Configs = collections.namedtuple("Configs", "wild_type")
    configs = Configs(wild_type=wild_type)
    return configs


class ParamParser:
    """Class docstring."""

    def __init__(self) -> None:
        pass

    def parse_params(self, args=None) -> argparse.Namespace:
        """Get the params
           Precedence is defaults < config files < cmdline

        When this finishes we return a Namespace that has these attributes
          - loglevel: how much info to log
          - mutants: directory for mutants
          - cmd_args: command arguments
          - bits: bit range
          - bytes: byte range
        """
        # TODO: update doc string

        parser = argparse.ArgumentParser(
            description="Brute-force survey of point mutants, every site in a span."
        )
        config_files = [SYSTEM_CONFIG, GLOBAL_CONFIG, LOCAL_CONFIG]
        defaults = config_parser(config_files)
        parser.add_argument(
            "--debug",
            help="Print DEBUG, INFO, WARNING, ERROR, CRITICAL",
            action="store_const",
            dest="loglevel",
            const=logging.DEBUG,
            default=logging.WARNING,
        )
        parser.add_argument(
            "--info",
            "--verbose",
            help="Print a lot: INFO, WARNING, ERROR, CRITICAL",
            action="store_const",
            dest="loglevel",
            const=logging.INFO,
            default=logging.WARNING,  # WARNING, ERROR, CRITICAL
        )
        parser.add_argument(
            "--wild_type",
            default=defaults.wild_type,
            help="un-mutated executable (default: %(default)s)",
        )
        parser.add_argument(
            "--mutants", help="directory to store mutants"
        )  # TODO: should this default to "mutants"?
        parser.add_argument(
            "--cmd_args", help="args for the executable(s)"
        )  # TODO: should this default to ""?

        bits_or_bytes = parser.add_mutually_exclusive_group()
        bits_or_bytes.add_argument(
            "--bits", help="bit(s) of interest", type=parsed_span
        )
        bits_or_bytes.add_argument(
            "--bytes", help="bytes(s) of interest", type=parsed_span
        )

        if args is None:
            args = []
        params = parser.parse_args(args)
        # set up logging
        logging.basicConfig(level=params.loglevel, format="%(message)s")
        logging.debug(params)

        # attribute validatation and enhancement
        params.wild_type = Path(params.wild_type)  # convert to a path
        assert params.wild_type.is_file(), f"No file {params.wild_type}"

        # bits and bytes
        params.size_in_bytes = Path(params.wild_type).stat().st_size
        params.size_in_bits = params.size_in_bytes * 8
        params.bits, params.bytes = bit_and_byte_ranges(params)

        return params
