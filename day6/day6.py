#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from functools import reduce
from operator import mul


@dataclass
class Race:
    duration: int
    distance: int

    def wins(self):
        w = 0
        for i in range(self.duration + 1):
            if i * (self.duration - i) > self.distance:
                w += 1
        return w


def part1(filename: str) -> None:
    with open(filename, "r") as f:
        durations = [int(v) for v in f.readline().split(": ")[1].split()]
        distances = [int(v) for v in f.readline().split(": ")[1].split()]

    races = [
        Race(duration, distance) for duration, distance in zip(durations, distances)
    ]
    print(reduce(mul, (race.wins() for race in races), 1))


def part2(filename: str) -> None:
    with open(filename, "r") as f:
        duration = int("".join(f.readline().split(": ")[1].split()))
        distance = int("".join(f.readline().split(": ")[1].split()))

    race = Race(duration, distance)

    print(race.wins())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
