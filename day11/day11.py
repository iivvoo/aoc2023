#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Self
import itertools


@dataclass
class Galaxy:
    r: int
    c: int

    def distance(self, other: Self) -> int:
        return abs(self.r - other.r) + abs(self.c - other.c)


class Universe:
    def __init__(self):
        self.rows: list[list[str]] = []
        self.galaxies: list[Galaxy] = []

    def add(self, row: str) -> None:
        self.rows.append(list(row))

    def expand(self) -> None:
        """expand rows and cols"""
        expand_rows = []
        for i, r in enumerate(self.rows):
            if set(r) == {"."}:
                expand_rows.append(i)

        for i in expand_rows[::-1]:
            self.rows.insert(i, ["."] * len(self.rows[0]))

        expand_cols = []
        for i in range(len(self.rows[0])):
            if set(r[i] for r in self.rows) == {"."}:
                expand_cols.append(i)

        for j in expand_cols[::-1]:
            for r in self.rows:
                r.insert(j, ".")

    def collect(self) -> None:
        """collect galaxies"""
        for r, row in enumerate(self.rows):
            for c, col in enumerate(row):
                if col == "#":
                    self.galaxies.append(Galaxy(r, c))

    def __str__(self) -> str:
        return "\n".join("".join(r) for r in self.rows)


def part1(filename: str) -> None:
    universe = Universe()

    for line in open(filename, "r"):
        universe.add(line.strip())

    universe.expand()
    universe.collect()

    s = 0

    for g, h in itertools.combinations(universe.galaxies, 2):
        s += g.distance(h)

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
