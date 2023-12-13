#!/usr/bin/env python3

import sys
from typing import List, Tuple


def countdiff(a: str, b: str) -> int:
    return sum(1 if a != b else 0 for (a, b) in zip(a, b))


class Terrain:
    def __init__(self):
        self.rows: List[str] = []

    def add(self, row: str) -> None:
        self.rows.append(row)

    def find_reflection(self, max_smudges=0) -> Tuple[int, int]:  # left, above
        # find vertical reflection
        for r in range(1, len(self.rows)):
            rnge = min(r, len(self.rows) - r)

            diffs = sum(
                countdiff(a, b)
                for (a, b) in zip(
                    self.rows[r - rnge : r], self.rows[r : r + rnge][::-1]
                )
            )
            if diffs == max_smudges:
                return 0, r

        # find horizontal reflection
        for c in range(1, len(self.rows[0])):
            rnge = min(c, len(self.rows[0]) - c)

            if (
                sum(
                    countdiff(row[c - rnge : c], row[c : c + rnge][::-1])
                    for row in self.rows
                )
                == max_smudges
            ):
                return c, 0

        return 0, 0

    def __str__(self) -> str:
        return "\n".join(self.rows)


def solve(filename: str, smudges=0) -> None:
    terrains = [Terrain()]
    for line in open(filename, "r"):
        if line == "\n":
            terrains.append(Terrain())
            continue
        terrains[-1].add(line.strip())

    s = 0
    for terrain in terrains:
        left, above = terrain.find_reflection(smudges)

        s += left + 100 * above

    print(s)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        solve(sys.argv[2])
    else:
        solve(sys.argv[2], smudges=1)
