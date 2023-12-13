#!/usr/bin/env python3

import sys
from typing import List, Tuple

"""
  aabbcc
  ddeeff
  ddeeff
  aabbcc

als ergens splits en rows joint,

aabbcc ddeeff ddeeff aabbcc
dus reverse 2e helft
"""


class Terrain:
    def __init__(self):
        self.rows: List[str] = []

    def add(self, row: str) -> None:
        self.rows.append(row)

    def find_reflection(self) -> Tuple[int, int]:
        # find vertical reflection
        for r in range(1, len(self.rows)):
            above = r
            below = len(self.rows) - r
            rnge = min(above, below)

            if self.rows[r - rnge : r] == self.rows[r : r + rnge][::-1]:
                return 0, r

        for c in range(1, len(self.rows[0])):
            before = c
            after = len(self.rows[0]) - c
            rnge = min(before, after)

            if all(row[c - rnge : c] == row[c : c + rnge][::-1] for row in self.rows):
                return c, 0

        return 0, 0

    def __str__(self) -> str:
        return "\n".join(self.rows)


def part1(filename: str) -> None:
    terrains = [Terrain()]
    for line in open(filename, "r"):
        if line == "\n":
            terrains.append(Terrain())
            continue
        terrains[-1].add(line.strip())

    s = 0
    for terrain in terrains:
        left, above = terrain.find_reflection()

        print(left, above)
        if left == above == 0:
            # breakpoint()
            left, above = terrain.find_reflection()

        s += left + 100 * above

    # 20561 is too low
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
