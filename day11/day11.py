#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Self
import itertools


@dataclass
class Galaxy:
    r: int
    c: int


class Universe:
    def __init__(self, expansion_rate: int = 2):
        self.rows: list[list[str]] = []
        self.galaxies: list[Galaxy] = []
        self.expanded_rows: list[int] = []
        self.expanded_cols: list[int] = []
        self.expansion_rate = expansion_rate

    def add(self, row: str) -> None:
        self.rows.append(list(row))

    def expand(self) -> None:
        """expand rows and cols"""
        for i, r in enumerate(self.rows):
            if set(r) == {"."}:
                self.expanded_rows.append(i)

        for i in range(len(self.rows[0])):
            if set(r[i] for r in self.rows) == {"."}:
                self.expanded_cols.append(i)


    def collect(self) -> None:
        """collect galaxies"""
        for r, row in enumerate(self.rows):
            for c, col in enumerate(row):
                if col == "#":
                    self.galaxies.append(Galaxy(r, c))

    def distance(self, one: Galaxy, other: Galaxy) -> int:
        d = 0
        for r in range(min(one.r, other.r), max(one.r, other.r)):
            if r in self.expanded_rows:
                d += self.expansion_rate
            else:
                d += 1

        for c in range(min(one.c, other.c), max(one.c, other.c)):
            if c in self.expanded_cols:
                d += self.expansion_rate
            else:
                d += 1
        return d


    def __str__(self) -> str:
        return "\n".join("".join(f"{r}") for r in self.rows)


def part1(filename: str) -> None:
    universe = Universe()

    for line in open(filename, "r"):
        universe.add(line.strip())

    universe.expand()
    universe.collect()

    answer = sum(universe.distance(g, h) for g, h in itertools.combinations(universe.galaxies, 2))

    print(answer)


def part2(filename: str, expansion_rate=1000000) -> None:
    universe = Universe(expansion_rate=expansion_rate)

    for line in open(filename, "r"):
        universe.add(line.strip())

    universe.expand()
    universe.collect()

    answer = sum(universe.distance(g, h) for g, h in itertools.combinations(universe.galaxies, 2))

    print(answer)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file> [expansion_rate]")
        sys.exit(1)

    expansion_rate = 1000000

    if len(sys.argv) == 4:
        expansion_rate = int(sys.argv[3])
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2], expansion_rate)
