#!/usr/bin/env python3

import sys
from dataclasses import dataclass, field
from functools import reduce


@dataclass(frozen=True)
class Position:
    r: int
    c: int


@dataclass(frozen=True)
class Step:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    position: Position
    direction: int


class Beam:
    ID = 0

    direction: int = Step.RIGHT
    steps: list[Step] = field(default_factory=list)
    dead: bool = False

    def __init__(self, direction: int, steps: list[Step], dead=False):
        self.direction = direction
        self.steps = steps
        self.dead = dead

        self.id = id
        self.ID += 1

    def __hash__(self) -> int:
        return hash(self.id)

    def advance(self, max_rows: int, max_cols: int):
        if self.dead:
            return

        last_step = self.steps[-1]
        last_pos = last_step.position

        next_pos = None

        if self.direction == Step.UP and last_pos.r > 0:
            next_pos = Position(last_pos.r - 1, last_pos.c)
        elif self.direction == Step.DOWN and last_pos.r < max_rows - 1:
            next_pos = Position(last_pos.r + 1, last_pos.c)
        elif self.direction == Step.LEFT and last_pos.c > 0:
            next_pos = Position(last_pos.r, last_pos.c - 1)
        elif self.direction == Step.RIGHT and last_pos.c < max_cols - 1:
            next_pos = Position(last_pos.r, last_pos.c + 1)
        else:
            self.dead = True

        if next_pos is not None:
            next_step = Step(next_pos, self.direction)
            self.steps.append(next_step)

    def clone(self) -> "Beam":
        return Beam(self.direction, self.steps.copy(), self.dead)


@dataclass(frozen=True)
class Splitter:
    HORIZONTAL = 1  # -
    VERTICAL = 2  # |

    position: Position
    direction: int

    def apply(self, beam: Beam) -> list[Beam]:
        if self.direction == Splitter.HORIZONTAL:
            if beam.direction in (Step.UP, Step.DOWN):
                left = beam.clone()
                left.direction = Step.LEFT
                beam.direction = Step.RIGHT
                return [left, beam]
        else:  # vertical
            if beam.direction in (Step.LEFT, Step.RIGHT):
                down = beam.clone()
                down.direction = Step.DOWN
                beam.direction = Step.UP
                return [beam, down]

        return [beam]  # it passes through


@dataclass(frozen=True)
class Mirror:
    FORWARD = 1  # /
    BACKWARD = 2  # \

    position: Position
    direction: int

    def apply(self, beam: Beam) -> Beam:
        if self.direction == Mirror.FORWARD:  # /
            if beam.direction == Step.RIGHT:
                beam.direction = Step.UP
            elif beam.direction == Step.LEFT:
                beam.direction = Step.DOWN
            elif beam.direction == Step.UP:
                beam.direction = Step.RIGHT
            elif beam.direction == Step.DOWN:
                beam.direction = Step.LEFT
        else:  # \
            if beam.direction == Step.RIGHT:
                beam.direction = Step.DOWN
            elif beam.direction == Step.LEFT:
                beam.direction = Step.UP
            elif beam.direction == Step.UP:
                beam.direction = Step.LEFT
            elif beam.direction == Step.DOWN:
                beam.direction = Step.RIGHT

        return beam


class Contraption:
    def __init__(self):
        self.mirrors: dict[Position, Mirror] = {}
        self.splitters: dict[Position, Splitter] = {}
        self.rows: list[str] = []

    def add(self, row: str) -> None:
        self.rows.append(row)
        for i, c in enumerate(row):
            p = Position(len(self.rows) - 1, i)
            if c == "/":
                self.mirrors[p] = Mirror(p, Mirror.FORWARD)
            if c == "\\":
                self.mirrors[p] = Mirror(p, Mirror.BACKWARD)
            if c == "-":
                self.splitters[p] = Splitter(p, Splitter.HORIZONTAL)
            if c == "|":
                self.splitters[p] = Splitter(p, Splitter.VERTICAL)

    def all_energized(self, beams: set[Beam]) -> set[Position]:
        return reduce(lambda a, b: a | set(s.position for s in b.steps), beams, set())

    def run(self, start: Step) -> int:
        beams = {Beam(start.direction, [start])}

        all_steps = set()

        while True:
            active = set()

            for beam in beams:
                if beam.dead:
                    continue

                if m := self.mirrors.get(beam.steps[-1].position):
                    active.add(m.apply(beam))
                elif s := self.splitters.get(beam.steps[-1].position):
                    active.update(s.apply(beam))
                else:
                    active.add(beam)

            for b in active:
                b.advance(len(self.rows), len(self.rows[0]))
                if b.steps[-1] in all_steps:
                    b.dead = True
                else:
                    all_steps.add(b.steps[-1])

            beams |= active
            if not active:
                break

        return len(self.all_energized(beams))

    def print(self, beams):
        all_energized = self.all_energized(beams)

        print("-" * 20)
        for i, row in enumerate(self.rows):
            for j, c in enumerate(row):
                if Position(i, j) in all_energized:
                    print("#", end="")
                else:
                    print(c, end="")
            print()
        print("-" * 10 + str(len(all_energized)) + "-" * 10)

    def __str__(self) -> str:
        return "\n".join(self.rows)


def part1(filename: str) -> None:
    c = Contraption()
    for row in open(filename, "r"):
        c.add(row.strip())

    print(c.run(Step(Position(0, 0), Step.RIGHT)))


def part2(filename: str) -> None:
    c = Contraption()
    for row in open(filename, "r"):
        c.add(row.strip())

    largest = 0

    for row in range(len(c.rows)):
        score = c.run(Step(Position(row, 0), Step.RIGHT))
        if score > largest:
            largest = score
        score = c.run(Step(Position(row, len(c.rows[0]) - 1), Step.LEFT))
        if score > largest:
            largest = score

    for col in range(len(c.rows[0])):
        score = c.run(Step(Position(0, col), Step.DOWN))
        if score > largest:
            largest = score
        score = c.run(Step(Position(0, len(c.rows) - 1), Step.UP))
        if score > largest:
            largest = score

    print(largest)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
