#!/usr/bin/env python3

import sys


class Dish:
    def __init__(self):
        self.rows: list[list[str]] = []

    def add(self, row: str) -> None:
        self.rows.append(list(row))

    def tilt(self) -> None:
        for i in range(1, len(self.rows)):
            for j, c in enumerate(self.rows[i]):
                if c != "O":
                    continue
                k = i
                while k > 0 and self.rows[k - 1][j] == ".":
                    self.rows[k - 1][j] = "O"
                    self.rows[k][j] = "."
                    k -= 1

    def score(self) -> int:
        return sum(r.count("O") * (len(self.rows) - i) for i, r in enumerate(self.rows))

    def __str__(self) -> str:
        return "\n".join("".join(r) for r in self.rows)


def part1(filename: str) -> None:
    d = Dish()

    for line in open(filename, "r"):
        d.add(line.strip())

    d.tilt()
    print(d.score())


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
