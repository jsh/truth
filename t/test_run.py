#!/usr/bin/env python3
"""Test utils module."""

import datetime

try:
    from run import run
except ImportError:
    import sys

    sys.path.append(".")
    from run import run

BADPATH = "/u/jane/me/tarzan"


def test_run_test_true():
    """simple success"""
    assert (0, "success", "", "") == run("true")


def test_run_test_false():
    """simple failure"""
    assert (1, "calledprocesserror", "", "") == run("false")


def test_run_success():
    """successful run produces expected results"""
    today = datetime.date.today().strftime("%F\n")
    returncode, outcome, out, err = run("date +%F")
    assert returncode == 0
    assert outcome == "success"
    assert out == today
    assert not err


def test_run_fail():
    """unsuccessful run produces calledprocesserror"""
    expected = (
        1,
        "calledprocesserror",
        "",
        "ls: {}: No such file or directory\n".format(BADPATH),
    )
    assert run("ls {}".format(BADPATH)) == expected


def test_run_badpath():
    """bad command produces filenotfounderror"""
    expected = (
        2,
        "filenotfounderror",
        None,
        "[Errno 2] No such file or directory: '{0}': '{0}'".format(BADPATH),
    )
    assert run(BADPATH) == expected


def test_run_timeout():
    """timeout produces timeoutexpired"""
    expected = (124, "timeoutexpired", None, None)
    assert run("sleep 2") == expected


def test_run_no_timeout():
    """timeout produces timeoutexpired"""
    expected = (0, "success", "", "")
    assert run("sleep 2", timeout=3) == expected
