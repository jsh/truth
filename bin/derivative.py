#!/usr/bin/env python3
"""
Record change points.

Given an input file that is a list of paired values, (x, y),
Report every line whose y value
doesn't equal that of the preceeding line,
and a count of the subsequent lines with that y value

For example:
    1 a
    2 a
    3 a
    5 b
    4 b
would be reported as
    3 ['1', 'a']
    2 ['4', 'b']
"""

import sys

last_value = ["", ""]
last_index = -1
index = -1
with open(sys.argv[1]) as fin:
    for line in fin:
        index += 1
        value = line.split()
        if value[1] != last_value[1]:
            span = index - last_index
            if index > 0:
                print(span, last_value)
            last_value = value
            last_index = index
index += 1
span = index - last_index
print(span, last_value)
