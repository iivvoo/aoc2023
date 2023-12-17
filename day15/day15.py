#!/usr/bin/env python3

import sys

def hash(s: bytes) -> int:
    v = 0
    for c in s:
        v += c
        v *= 17
        v %= 256
    return v
        
def part1(filename: str) -> None:
    input = open(filename, "rb").readline().strip()
    parts = input.split(b",")

    print(sum(hash(p) for p in parts))


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
