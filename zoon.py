#!/usr/bin/env python3
"""An executable, treated like a living entity."""

import array
from pathlib import Path
from typing import List, Tuple

# pylint: disable=ungrouped-imports
import run
from utils import adjusted, excess, to_bytes, toggle_bit_in_byte


class Zoon:
    """Create a Zoon from a file, a string, or another Zoon
    :param str or Zoon: string of filename or {0,1} or another Zoon
    :param bool fromfile: is this coming from a file?
    """

    def __init__(self, initializer, fromfile: bool = True):
        """Instantiate a Zoon.
        """
        self._initializer = initializer
        self._fromfile = fromfile
        self.__byteseq = array.array("B")  # array of unsigned chars
        if fromfile:
            path = Path(initializer)
            assert path.is_file()
            with open(initializer, "rb") as fin:
                self.__byteseq.fromfile(fin, path.stat().st_size)
        elif isinstance(initializer, str):
            assert set(initializer) <= {"0", "1"}
            self.__byteseq.frombytes(to_bytes(initializer))
        elif isinstance(initializer, Zoon):
            self.__byteseq.extend(initializer.byteseq)
        else:
            raise TypeError

    @property
    def byteseq(self) -> array.array:
        """When you really need the underlying array.
        :returns: The bytearray
        :rtype: array.array
        """
        return self.__byteseq

    @byteseq.setter
    def byteseq(self, new_list: List[int]):
        """When you really need the underlying array.
        :param list[int] new_list: The new bytearray
        """
        self.__byteseq = array.array("B", new_list)

    def __len__(self) -> int:
        """Return the length in bits.
        :returns: length in bits
        :rtype: int
        """
        return len(self.__byteseq) * 8

    def __repr__(self) -> str:
        """return something that looks just like the object."""
        return f"zoon.Zoon('{self._initializer}', fromfile={self._fromfile})"

    def write(self, filename: Path):
        """Write Zoon to file.
        :param str filename: The name of the file to write.
        """
        with open(filename, "wb") as fout:
            self.__byteseq.tofile(fout)

    def mutate(self, position: int):
        """Point-mutate Zoon bytes at the given position.
        :param int position: the position of the point mutation
        :return: mutant
        :rtype: zoon.Zoon
        assert position >= 0
        return new array with bitflip at position
        TODO: exception if position > len(Zoon)
        """
        byte, bit = divmod(position, 8)
        mutant = Zoon(self, fromfile=False)
        mutant.byteseq[byte] = toggle_bit_in_byte(7 - bit, mutant.byteseq[byte])
        return mutant

    def run(self, timeout: int = 1, args: str = "") -> Tuple[int, str, str, str]:
        """Run the Zoon.
        :param int timeout: timeout in seconds
        :param bool output: provide output
        :raises: Exception if timeout
        :return: the exit status, optionally the output
        :rtype: tuple(int, str, str, str)
        run for timeout seconds, max
        """
        assert timeout > 0
        output_dir = Path("bin")
        output_dir.mkdir(exist_ok=True)
        mutant_path = (
            output_dir / "mutant"
        )  # could be a tempfile, but it's useful to keep the last one
        self.write(mutant_path)
        mutant_path.chmod(0o755)
        command = "%s %s" % (mutant_path, args) if args else str(mutant_path)
        return run.run(command, timeout=timeout)

    # nothing below this implemented

    def delete(self, start: int, stop: int):  # -> object:  # TODO: define Zoon type
        """Delete slice from start to stop
        :param int start: starting bit
        :param int stop: end bit (open interval)
        :returns: mutant
        :rtype: zoon.Zoon
        TODO: range checks
        """
        mutant = Zoon(self, fromfile=False)
        byteseq = mutant.byteseq
        if excess(start):
            requested_start = start
            start = adjusted(start)
            print(f"start must be at byte boundary. {requested_start} -> {start}")
        if excess(stop):
            requested_stop = stop
            stop = adjusted(stop)
            print(f"stop must be at byte boundary. {requested_stop} -> {stop}")

        start_byte = start // 8
        stop_byte = stop // 8
        mutant.byteseq = byteseq[:start_byte] + byteseq[stop_byte:]
        return mutant

    # nothing below this implemented

    def __str__(self):
        """Print something more attractive."""

    def insert(self, position, insertion):
        """Return new Zoon with insertion (a Zoon)
        :param int position: position of insertion
        :param Zoon insertion: The chunk to insert
        :returns: new Zoon with insertion inserted
        :rtype: Zoon
        """

    def invert(self, chunk):
        """Invert a chunk of the Zoon
        :param slice chunk:
        :returns: new Zoon with chunk inverted
        :rtype: Zoon

        assert isinstance(slice, Slice)
        invert the slice
        """

    def cross(self, other, position):
        """Return a new Zoon that's self[:position] + other[position:]
        :param Zoon other: The other Zoon to cross with
        :param int position: Where to cross-over
        :returns: the recombinant
        :rtype: Zoon
        """
