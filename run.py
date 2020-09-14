#!/usr/bin/env python3
"""Module docstring."""

import shlex
import subprocess
from typing import Tuple


def run(command: str, timeout: int = 1) -> Tuple[int, str, str, str]:
    """Run the command and record the result.
    :param str command:
    :param int timeout: # timeout
    :returns: result of the run
    :rtype: tuple(int, str, str, str)
    """

    cmd = shlex.split(command)

    try:
        output = subprocess.run(
            cmd, timeout=timeout, capture_output=True, text=True, check=True
        )
        returncode = output.returncode
        outcome = "success"
        out = output.stdout
        err = output.stderr
    except FileNotFoundError as exc:
        returncode = 2
        outcome = "filenotfounderror"
        out = ""
        err = str(exc)
    except PermissionError as exc:
        returncode = 126
        outcome = "permissionerror"
        out = ""
        err = str(exc)
    except subprocess.CalledProcessError as exc:
        returncode = exc.returncode
        outcome = "calledprocesserror"
        out = exc.stdout
        err = exc.stderr
    except OSError as exc:
        returncode = -2
        outcome = "oserror"
        out = ""
        err = str(exc)
    except subprocess.TimeoutExpired as exc:
        returncode = 124
        outcome = "timeoutexpired"
        out = exc.stdout
        err = exc.stderr
    except Exception as exc:  # some other misfortune
        returncode = -1
        outcome = "exception"
        out = ""
        err = str(exc)
    return (returncode, outcome, out, err)
