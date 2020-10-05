# /!/usr/bin/env python3
"""Test run module."""

import datetime
import sys

from run import run
from utils import which

BADPATH = "/u/jane/me/tarzan"
# pylint:disable=arguments-differ


def platform():
    """Return platform name.
    :return: the platform name
    :rtype: str
    """
    # TODO: this should be generic setup code with an @
    # TODO: this should, perhaps, be a table somewhere
    this_platform = sys.platform
    assert this_platform in {
        "darwin",
        "linux",
    }, "Platform {platform} must be 'darwin' or 'linux'"
    return this_platform


def test_run_test_true() -> None:
    """Simple success."""
    expected = (0, "success", "", "")
    assert run(str(which("true"))) == expected


def test_run_test_false() -> None:
    """Simple failure."""
    false = str(which("false"))
    expected = (
        1,
        "calledprocesserror",
        "",
        f"Command '['{false}']' returned non-zero exit status 1.",
    )
    assert run(str(which("false"))) == expected


def test_run_success() -> None:
    """Successful run produces expected results."""
    today = datetime.date.today().strftime("%F\n")
    expected = (0, "success", today, "")
    assert run("date +%F") == expected


# def test_run_fail() -> None:
#     """Unsuccessful run produces calledprocesserror."""
#     observed = run(f"ls {BADPATH}")
#
#     assert observed[0] == 1 if platform == "darwin" else 2
#     assert observed[1:3] == ("calledprocesserror", "")
#     expected = ( "Command '['ls', '/u/jane/me/tarzan']'
#         returned non-zero exit status 1.")
#     if platform() == "darwin":
#         assert observed[3] == expected
#     else:
#         assert "No such file or directory\n" in observed[3]
#
#
def test_run_badpath() -> None:
    """bad command produces filenotfounderror."""
    expected = (
        2,
        "filenotfounderror",
        "",
        f"[Errno 2] No such file or directory: '{BADPATH}'",
    )
    observed = run(BADPATH)
    assert observed[:2] == expected[:2]
    assert expected[3] in observed[3]


def test_run_timeout() -> None:
    """Timeout produces timeoutexpired."""
    expected = (124, "timeoutexpired", "", "")
    assert run("sleep 2") == expected


def test_run_no_timeout() -> None:
    """Timeout produces timeoutexpired."""
    expected = (0, "success", "", "")
    assert run("sleep 2", timeout=3) == expected


def test_run_permission_denied() -> None:
    """Run something without perms produces permissionerror."""
    expected = (
        126,
        "permissionerror",
        "",
        "[Errno 13] Permission denied: '/etc/passwd'",
    )
    assert run("/etc/passwd") == expected


def test_run_file_not_found() -> None:
    """Run something not a file produces filenotfounderror."""
    expected = (2, "filenotfounderror", "", "[Errno 2] No such file or directory: '<>'")
    observed = run("<>")
    assert observed[:2] == expected[:2]
    assert expected[3] in observed[3]


# def test_run_oserror() -> None:
#     """Run something not a file produces OSError."""
#     # TODO: create the executable and put in a temporary directory
#     expected = (126, "oserror", "", "[Errno 8] Exec format error: 't/bin/badexe'")
#     assert run("t/bin/badexe") == expected
#
#
def test_run_with_args() -> None:
    """Run something with args"""

    output_lines = [
        "true (GNU coreutils) 8.32",
        "Copyright (C) 2020 Free Software Foundation, Inc.",
        (
            "License GPLv3+: GNU GPL version 3 or later"
            " <https://gnu.org/licenses/gpl.html>."
        ),
        "This is free software: you are free to change and redistribute it.",
        "There is NO WARRANTY, to the extent permitted by law.",
        "",
        "Written by Jim Meyering.",
        "",
    ]
    output_msg = "\n".join(output_lines)
    expected = (0, "success", output_msg, "")
    if platform() == "darwin":
        assert run(str("gtrue --version")) == expected
    else:
        assert run(str("true --version")) == expected
