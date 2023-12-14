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
        if reverse:
            return "#".join("."*x.count(".") + "O"*x.count("O") for x in "".join(line).split("#"))
        return "#".join("O"*x.count("O") + "."*x.count(".") for x in "".join(line).split("#"))

    def tilt(self, direction: Direction) -> None:
        if direction in [Direction.NORTH, Direction.SOUTH]:
            reverse = direction == Direction.SOUTH

            for c in range(len(self.rows[0])):
                before = [r[c] for r in self.rows]
                titled = self.tilt_line(before, reverse)
                                        
                for i, t in enumerate(titled):
                    self.rows[i][c] = t
        else:
            reverse = direction == Direction.WEST
            for i, r in enumerate(self.rows):
                self.rows[i] = list(self.tilt_line(r, reverse))


    def score(self) -> int:
        return sum(r.count("O") * (len(self.rows) - i) for i, r in enumerate(self.rows))

    def __str__(self) -> str:
        return "\n".join("".join(r) for r in self.rows)


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

    # find when repetition happens
    # 
    values = []
    def isrepeating(v):
        for i in range(100, len(v) - 100):
            print(len(v[1:101]), len(v[i+1:i+101]))
            if v[1:101] == v[i+1:i+101]:
                return i
        return -1

    for i in range(5000):
        d.tilt(direction=Direction.NORTH)
        d.tilt(direction=Direction.EAST)
        d.tilt(direction=Direction.SOUTH)
        d.tilt(direction=Direction.WEST)
        values.append(d.score())

        if r := isrepeating(values) != -1:
            print("Repeating at ", r)
            break


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
