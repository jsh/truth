#!/usr/bin/env python3
"""Run an executable
1 - Catchall for general errors
2 - Misuse of shell builtins (according to Bash documentation)
126 - Command invoked cannot execute
127 - “command not found”
128 - Invalid argument to exit
128+n - Fatal error signal “n”
130 - Script terminated by Control-C
-1 - Same as 254 == -1 mod 256
> 255 - Exit status out of range

See https://tldp.org/LDP/abs/html/exitcodes.html
See also /usr/include/sysexits.h
"""

import shlex
import subprocess
from subprocess import PIPE
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
            cmd,
            timeout=timeout,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
            check=True,
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
    except subprocess.TimeoutExpired:
        returncode = 124
        outcome = "timeoutexpired"
        out = ""
        err = ""
    except Exception as exc:  # some other misfortune
        returncode = -1
        outcome = "exception"
        out = ""
        err = str(exc)
    return (returncode, outcome, out, err)
