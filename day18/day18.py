#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from enum import Enum
import itertools


@dataclass
class Instruction:
    direction: str
    steps: int
    color: str

    def __init__(self, direction: str, steps: int):
        self.direction = direction
        self.steps = steps

    @classmethod
    def FromString(cls, s: str) -> "Instruction":
        parts = s.strip().split()
        direction = parts[0]
        steps = int(parts[1])

        return cls(direction, steps)

    @classmethod
    def FromString2(cls, s: str) -> "Instruction":
        instr = s.strip().split()[-1]

        hexlength = instr[2:-2]
        hexdir = instr[-2]

        direction = "RDLU"[int(hexdir)]
        steps = int(hexlength, 16)
        return cls(direction, steps)

    def __str__(self) -> str:
        return f"{self.direction} {self.steps}"


class Lagoon:
    def __init__(self):
        self.digs = {}

    def dig(self, instructions: list[Instruction]) -> None:
        r, c = (0, 0)

        for instr in instructions:
            if instr.direction == "R":
                for _ in range(instr.steps):
                    self.digs[(r, c)] = "#"
                    c += 1
            if instr.direction == "L":
                for _ in range(instr.steps - 1, -1, -1):
                    self.digs[(r, c)] = "#"
                    c -= 1
            if instr.direction == "U":
                for _ in range(instr.steps - 1, -1, -1):
                    self.digs[(r, c)] = "#"
                    r -= 1
            if instr.direction == "D":
                for _ in range(instr.steps):
                    self.digs[(r, c)] = "#"
                    r += 1

    def plot(self, instructions: list[Instruction]) -> None:
        r, c = (0, 0)

        self.digs[(r, c)] = 0

        for instr in instructions:
            if instr.direction == "R":
                c += instr.steps

            if instr.direction == "L":
                c -= instr.steps

            if instr.direction == "U":
                r -= instr.steps

            if instr.direction == "D":
                r += instr.steps

            self.digs[(r, c)] = instr.steps

    def fill(self, r=1, c=1):
        stack = [(r, c)]

        while stack:
            (r, c) = stack.pop()

            if self.digs.get((r, c)):
                continue

            self.digs[(r, c)] = "$"

            stack.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])

    def print(self) -> None:
        min_r = min(r for r, _ in self.digs.keys())
        min_c = min(c for _, c in self.digs.keys())
        max_r = max(r for r, _ in self.digs.keys())
        max_c = max(c for _, c in self.digs.keys())

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r, c) in self.digs:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def shoelace(self):
        points = list(self.digs.keys())

        s = sum(
            (x1 * y2) - (y1 * x2) for (y1, x1), (y2, x2) in itertools.pairwise(points)
        )

        return int((s + sum(d for d in self.digs.values()) + 2) / 2)


def part1(filename: str) -> None:
    instructions: list[Instruction] = []

    for line in open(filename, "r"):
        instructions.append(Instruction.FromString(line))

    l = Lagoon()
    l.dig(instructions)
    l.print()
    l.fill(1, 1)
    print()
    l.print()
    print(len(l.digs))


def part2(filename: str) -> None:
    instructions: list[Instruction] = []

    for line in open(filename, "r"):
        instructions.append(Instruction.FromString2(line))

    l = Lagoon()
    l.plot(instructions)
    print(l.shoelace())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
