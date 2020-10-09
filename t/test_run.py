# /!/usr/bin/env python3
"""Test run module."""

import datetime
import os
import sys
from pathlib import Path

import pytest  # type: ignore

from run import run
from utils import which

# pylint:disable=arguments-differ


def platform():
    """Return platform name.
    :return: the platform name
    :rtype: str
    """
    # TODO: this should be generic setup code with an @
    # TODO: this should, perhaps, be a table somewhere
    # TODO: move into utils?
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
#     badpath = "/u/jane/me/tarzan"
#     observed = run(f"ls {badpath}")
#
#     assert observed[0] == 1 if platform == "darwin" else 2
#     assert observed[1:3] == ("calledprocesserror", "")
#     expected = ( f"Command '['ls', '{badpath}']'
#         returned non-zero exit status 1.")
#     if platform() == "darwin":
#         assert observed[3] == expected
#     else:
#         assert "No such file or directory\n" in observed[3]
#
#
def test_run_badpath() -> None:
    """bad command produces filenotfounderror."""
    badpath = "/u/jane/me/tarzan"
    expected = (
        2,
        "filenotfounderror",
        "",
        f"[Errno 2] No such file or directory: '{badpath}'",
    )
    observed = run(badpath)
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


@pytest.fixture()
def bad_exe(tmpdir):
    """Create a bad executable."""
    src_file = str(tmpdir / "bad_src.h")
    exe_file = str(tmpdir / "bad_exe")
    open(src_file, "w").close()
    os.system(f"cc {src_file} -o {exe_file}")
    Path(exe_file).chmod(0o755)
    return exe_file


def test_run_oserror(bad_exe) -> None:  # pylint:disable=redefined-outer-name
    """Run something not a file produces OSError."""
    # TODO: Make this portable
    if platform() == "darwin":
        expected = (126, "oserror", "", f"[Errno 8] Exec format error: '{bad_exe}'")
        assert run(bad_exe)[:3] == expected[:3]


def test_run_with_args() -> None:
    """Run something with args"""

    output_lines = [
        "This is free software: you are free to change and redistribute it.",
        "There is NO WARRANTY, to the extent permitted by law.",
        "",
        "Written by Jim Meyering.",
        "",
    ]
    output_msg = "\n".join(output_lines)
    expected = (0, "success", output_msg, "")
    # check stdout
    true = "gtrue" if platform() == "darwin" else "true"
    observed = run(f"{true} --version")
    assert expected[2] in observed[2]
    # check the rest
    for field in [0, 1, 3]:
        assert expected[field] == observed[field]
