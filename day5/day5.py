#!/usr/bin/env python3

import sys
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class SingleMap:
    dest: int
    source: int
    range: int

    def map(self, seed: int) -> Tuple[int, bool]:
        if seed >= self.source and seed < self.source + self.range:
            return self.dest + seed - self.source, True

        return -1, False


@dataclass
class Mapping:
    name: str
    single_maps: list[SingleMap] = field(default_factory=list)

    def map(self, seed: int) -> int:
        for single_map in self.single_maps:
            mapped, success = single_map.map(seed)
            if success:
                return mapped

        return seed


def parse(filename: str) -> Tuple[list[int], dict[str, Mapping]]:
    mappings: dict[str, Mapping] = {}
    current: Mapping | None = None

    seeds: list[int] = []

    with open(filename) as f:
        for line in f.readlines():
            if line.strip() == "":
                continue
            if line.startswith("seeds:"):
                seeds = list(map(int, line.split()[1:]))
                continue

            if line.strip().endswith("map:"):
                mapping = line.split()[0]
                current = mappings[mapping] = Mapping(mapping)
                continue

            values = map(int, line.split())
            assert current is not None
            current.single_maps.append(SingleMap(*values))

    return seeds, mappings


def lowest(seeds: list[int], mappings: dict[str, Mapping]) -> int:
    lowest = -1

    for seed in seeds:
        for mapping in (
            "seed-to-soil",
            "soil-to-fertilizer",
            "fertilizer-to-water",
            "water-to-light",
            "light-to-temperature",
            "temperature-to-humidity",
            "humidity-to-location",
        ):
            seed = mappings[mapping].map(seed)
        if lowest == -1 or seed < lowest:
            lowest = seed

    return lowest


def part1(filename: str) -> None:
    seeds, mappings = parse(filename)
    print(lowest(seeds, mappings))


from concurrent.futures import ProcessPoolExecutor


def part2(filename: str) -> None:
    seeds, mappings = parse(filename)

    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(lowest, list(range(s, s + l)), mappings)
            for (s, l) in zip(seeds[::2], seeds[1::2])
        ]
        results = [future.result() for future in futures]

    print(min(results))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
