#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import List
from collections import defaultdict


@dataclass
class Card:
    wins: List[int]
    haves: List[int]

    def __init__(self, line):
        have, wins = line.split(": ")[1].split(" | ")
        self.wins = [int(v) for v in wins.split()]
        self.haves = [int(v) for v in have.split()]
        self.matches = set(self.wins) & set(self.haves)


def part1(filename):
    s = 0
    with open(filename, "r") as f:
        for l in f.readlines():
            card = Card(l)
            matches = len(card.matches)
            if matches:
                s += 2 ** (matches - 1)

    print(s)


def part2(filename):
    cards = []
    with open(filename, "r") as f:
        for l in f.readlines():
            card = Card(l)
            cards.append(card)

    counts = defaultdict(lambda: 1)
    for i, card in enumerate(cards):
        amount = counts[i]
        matches = len(card.matches)
        if matches:
            for extra in range(matches):
                counts[i + extra + 1] += amount

    print(sum(counts.values()))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
