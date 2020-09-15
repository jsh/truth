#!/usr/bin/env python3
"""Record change points."""

import sys

lines = sys.stdin.readlines()

values = [line.rstrip() for line in lines]
values.append("This is a sentine!")  # a sentinel

last_value = None
last_index = -1
for index, value in enumerate(values):
    if value != last_value:
        span = index - last_index
        if index > 0:
            print(last_value, span)
        last_value = value
        last_index = index
