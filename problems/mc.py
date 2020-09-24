#!/usr/bin/env python3
"""Module docstring."""


class MyClass:
    """Class docstring."""

    def __init__(self, value: int) -> None:
        """Function docstring."""
        self._value = value

    def value(self) -> int:
        """Function docstring."""
        return self._value

    def bigger(self) -> MyClass:
        """Function docstring."""
        return MyClass(self.value + 1)


mc = MyClass(69)
print(f"myclass.value(): {mc.value()}")
huge = mc.bigger()
print(f"huge.value(): {huge.value()}")
