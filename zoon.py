#!/usr/bin/env python3
"""An executable, treated like a living entity."""

from array import array
from pathlib import Path

# pylint: disable=ungrouped-imports
try:
    import run
    from utils import to_bytes, toggle_bit_in_byte
except ImportError:
    import sys

    sys.path.append(".")
    import run
    from utils import to_bytes, toggle_bit_in_byte


class Zoon:
    """Create a Zoon from a file, a string, or another Zoon
    :param str or Zoon: string of filename or {0,1} or another Zoon
    :param bool fromfile: is this coming from a file?
    """

    def __init__(self, initializer, fromfile=True):
        """Instantiate a Zoon.
        """
        self._initializer = initializer
        self._fromfile = fromfile
        self._bytes = array("B")  # array of unsigned chars
        if fromfile:
            path = Path(initializer)
            assert path.is_file()
            with open(initializer, "rb") as fin:
                self._bytes.fromfile(fin, path.stat().st_size)
        elif isinstance(initializer, str):
            assert set(initializer) <= {"0", "1"}
            self._bytes.frombytes(to_bytes(initializer))
        elif isinstance(initializer, Zoon):
            self._bytes.extend(initializer.bytes())
        else:
            raise TypeError

    def bytes(self):
        """When you really need the underlying array.
        :returns: The bytearray
        :rtype: array.array
        """
        return self._bytes

    def __len__(self):
        """Return the length in bits.
        :returns: length in bits
        :rtype: int
        """
        return len(self._bytes) * 8

    def __repr__(self):
        """return something that looks just like the object."""
        return f"zoon.Zoon('{self._initializer}', fromfile={self._fromfile})"

    def write(self, filename):
        """Write Zoon to file.
        :param str filename: The name of the file to write.
        """
        with open(filename, "wb") as fout:
            self._bytes.tofile(fout)

    def mutate(self, position):
        """Point-mutate Zoon bytes at the given position.
        :param int position: the position of the point mutation
        assert position >= 0
        return new array with bitflip at position
        exception if position > len(Zoon)
        """
        byte, bit = divmod(position, 8)
        mutant = Zoon(self, fromfile=False)
        mutant.bytes()[byte] = toggle_bit_in_byte(7 - bit, mutant.bytes()[byte])
        return mutant

    # nothing below this implemented

    def __str__(self):
        """Print something more attractive."""

    def run(self, timeout=1, args=""):
        """Run the Zoon.
        :param int timeout: timeout in seconds
        :param bool output: provide output
        :raises: Exception if timeout
        :return: the exit status, optionally the output
        :rtype: collections.namedtuple
        assert time > 0
        run for time seconds, max
        return tuple (exit_status, output), output iff output=True
        exception if timeout
        """
        assert timeout > 0
        mutant = Path(
            "mutant"
        )  # could be a tempfile, but it's useful to keep the last one
        with open(mutant, "w+b") as fout:
            self._bytes.tofile(fout)
        mutant.chmod(0o755)
        command = "%s %s" % (mutant, args) if args else "mutant"
        return run.run(command, timeout=timeout)

    def delete(self, chunk):
        """Delete a slice from a Zoon
        :param slice chunk:
        :returns: new Zoon with chunk deleted
        :rtype: Zoon
        assert isinstance(chunk, slice)
        delete a slice from the bitarray
        return new Zoon
        """

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
