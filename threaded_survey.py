#!/usr/bin/env python3
"""Drive the truth."""

import atexit
import queue
import shutil
import sys
import tempfile
import threading
import time
from pathlib import Path
from queue import Queue
from typing import Tuple

from parse_args import get_args
from utils import which
from zoon import Zoon

Result = Tuple[int, str, str, str]


def threader():
    """pull a worker from the queue and process it"""

    while True:
        # get a worker from the queue
        bit = my_queue.get()

        # run the task with an available thread (worker) in the queue
        result = zoon.mutate_and_run(position=bit, fs_path=fs_path)
        report(result, bit, verbose=False)  # TODO: get global args

        # done with the thread
        my_queue.task_done()


def survey_range(args) -> None:
    """Mutatate the wild type at each bit in a range and capture the results.
    :param args.Namespace args: All the args
    """

    for _ in range(args.threads):
        thread = threading.Thread(target=threader)
        # classifying it as a daemon, so it will die when main() dies
        thread.daemon = True
        # begin, must come after daemon definition
        thread.start()
    for bit in range(args.bits.start, args.bits.end):
        my_queue.put(bit)
    # wait until threads terminate
    my_queue.join()


def report(result: Result, bit, verbose=False) -> None:
    """Report the results.
    :param list results: results to report
    :param int bit: mutated bit
    :param bool verbose: chatty or terse?
    """
    if verbose:
        print(f"mutant at bit {bit}: {result}")
    else:
        if result:
            print(f"{bit}\t{result[0]}")


def main(argv: list) -> None:
    """The big tent.
    :param list argv: All the args. sys.argv
    """
    args = get_args(
        "Brute-force survey of point mutants, every site in a span.", argv[1:]
    )
    if args.verbose:
        print(args, file=sys.stderr)

    start = time.time()
    survey_range(args)
    end = time.time()
    elapsed_time = end - start
    nmutants = args.bits.end - args.bits.start - 1
    if args.verbose:
        print(
            f"processed {nmutants} mutants with {args.threads} thread(s) in {elapsed_time} seconds",
            file=sys.stderr,
        )


if __name__ == "__main__":

    # TODO: globals. this is fucked.  Fix.
    my_queue: Queue = queue.Queue()
    tempdir = tempfile.mkdtemp()  # use a temporary directory, then cleanup
    atexit.register(shutil.rmtree, tempdir)
    fs_path = Path(tempdir)
    zoon = Zoon(which("true"))
    main(sys.argv)
# try:
#     main(sys.argv)
# except Exception as exc:
#     print(f"Unexpected exception: {str(exc)}")
