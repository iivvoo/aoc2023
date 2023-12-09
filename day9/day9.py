#!/usr/bin/env python3

import sys


def predict(values: list[int]) -> int:
    p = values[-1]
    while values.count(values[0]) != len(values):
        values = [b-a for a, b in zip(values, values[1:])]
        p += values[-1]
    return p

def part1(filename: str) -> None:
    s = 0
    for line in open(filename, "r"):
        values = [int(v) for v in line.split()]
        s += predict(values)
    print(s)

def part2(filename: str) -> None:
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
