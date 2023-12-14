#!/usr/bin/env python3

import sys
from enum import Enum


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class Dish:
    def __init__(self):
        self.rows: list[list[str]] = []

    def add(self, row: str) -> None:
        self.rows.append(list(row))

    def tilt_line(self, line, reverse=False) -> str:
        parts = "".join(line).split("#")
        if reverse:
            return "#".join("." * x.count(".") + "O" * x.count("O") for x in parts)
        return "#".join("O" * x.count("O") + "." * x.count(".") for x in parts)

    def tilt(self, direction: Direction) -> None:
        if direction in [Direction.NORTH, Direction.SOUTH]:
            reverse = direction == Direction.SOUTH

            for c in range(len(self.rows[0])):
                titled = self.tilt_line([r[c] for r in self.rows], reverse)

                for i, t in enumerate(titled):
                    self.rows[i][c] = t
        else:
            reverse = direction == Direction.WEST
            for i, r in enumerate(self.rows):
                self.rows[i] = list(self.tilt_line(r, reverse))

    def score(self) -> int:
        return sum(r.count("O") * (len(self.rows) - i) for i, r in enumerate(self.rows))


def part1(filename: str) -> None:
    d = Dish()

    for line in open(filename, "r"):
        d.add(line.strip())

    d.tilt(direction=Direction.NORTH)
    print(d.score())


def part2(filename: str) -> None:
    d = Dish()

    for line in open(filename, "r"):
        d.add(line.strip())

    def isrepeating(v: list[int], psize: int) -> int:
        # psize is the size of the pattern at the end that we try to find earlier in v
        if len(v) < psize * 3:
            return -1

        pattern = v[-psize:]
        for i in range(len(v) - psize - 1, psize, -1):
            if v[i : i + psize] == pattern:
                return i
        return -1

    # values are a bit trial/error - they have to be largish enough to find a
    # confident repetition
    psize = 50
    values = []

    while True:
        for dir in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            d.tilt(direction=dir)
        values.append(d.score())

        if (r := isrepeating(values, psize)) != -1:
            # r is where the repetition starts, len(values) - psize - r is the length of the full rep
            idx = (1000_000_000 - r - 1) % (len(values) - psize - r)
            print(values[r + idx])
            break


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
