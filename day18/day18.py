#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from enum import Enum


@dataclass
class Instruction:
    direction: str
    steps: int
    color: str

    def __init__(self, direction: str, steps: int, color: str):
        self.direction = direction
        self.steps = steps
        self.color = color

    @classmethod
    def FromString(cls, s: str) -> "Instruction":
        parts = s.strip().split()
        direction = parts[0]
        steps = int(parts[1])
        color = parts[2]

        return cls(direction, steps, color)


class Lagoon:
    def __init__(self):
        self.digs = {}

    def dig(self, instructions: list[Instruction]) -> None:
        r, c = (0, 0)

        for instr in instructions:
            if instr.direction == "R":
                for i in range(instr.steps):
                    self.digs[(r, c)] = instr.color
                    c += 1
            if instr.direction == "L":
                for i in range(instr.steps - 1, -1, -1):
                    self.digs[(r, c)] = instr.color
                    c -= 1
            if instr.direction == "U":
                for i in range(instr.steps - 1, -1, -1):
                    self.digs[(r, c)] = instr.color
                    r -= 1
            if instr.direction == "D":
                for i in range(instr.steps):
                    self.digs[(r, c)] = instr.color
                    r += 1

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
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
