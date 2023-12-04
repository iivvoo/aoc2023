#!/usr/bin/env python3

import sys


def part1(filename):
    s = 0
    with open(filename, "r") as f:
        for l in f.readlines():
            have, winning = l.split(": ")[1].split(" | ")
            matches = len(
                set(int(w) for w in winning.split()) & set(int(h) for h in have.split())
            )
            if matches:
                s += 2 ** (matches - 1)

    print(s)


def part2(filename):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
