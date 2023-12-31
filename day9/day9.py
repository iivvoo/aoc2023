#!/usr/bin/env python3

import sys
from functools import reduce
from itertools import pairwise

def predict(values: list[int]) -> int:
    p = values[-1]
    while values.count(values[0]) != len(values):
        values = [b - a for a, b in pairwise(values)]
        p += values[-1]
    return p


def predict2(values: list[int]) -> int:
    befores = [values[0]]

    while values.count(values[0]) != len(values):
        values = [b - a for a, b in pairwise(values)]
        befores.insert(0, values[0])

    v = reduce(lambda a, b: b - a, befores)
    return v


def part1(filename: str) -> None:
    s = 0
    for line in open(filename, "r"):
        values = [int(v) for v in line.split()]
        s += predict(values)
    print(s)


def part2(filename: str) -> None:
    print(sum(predict2([int(v) for v in line.split()]) for line in open(filename, "r")))


def part2_smart(filename: str) -> None:
    # didn't realize this myself
    s = 0
    for line in open(filename, "r"):
        values = [int(v) for v in line.split()]
        s += predict(values[::-1])
    print(s)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    elif sys.argv[1] == "2":
        part2(sys.argv[2])
    else:
        part2_smart(sys.argv[2])
