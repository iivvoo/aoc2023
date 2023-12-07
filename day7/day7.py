#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from functools import total_ordering
from typing import List
from enum import IntEnum
import collections


class Type(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    FIVE_OF_A_KIND = 9


# A K Q J T 9 .. 2

values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass
@total_ordering
class Card:
    Label: str

    def __lt__(self, other: "Card") -> bool:
        return values[self.Label] < values[other.Label]

    def __eq__(self, other: "Card") -> bool:
        return values[self.Label] == values[other.Label]

    def __hash__(self) -> int:
        return values[self.Label]


@dataclass
@total_ordering
class Hand:
    cards: List[Card]

    """
        Determine type, where type also maps to a value, the higher the better

        Sort Cards first? -> 12345 LLKKK etc
        Group by equals -> LL KKK  / 1 2 3 4 5


    """

    def type(self) -> Type:
        counts = collections.defaultdict(int)
        for c in self.cards:
            counts[c] += 1
        vals = sorted(counts.values())

        if vals == [5]:
            return Type.FIVE_OF_A_KIND
        if vals == [1, 4]:
            return Type.FOUR_OF_A_KIND
        if vals == [2, 3]:
            return Type.FULL_HOUSE
        if 3 in vals:
            return Type.THREE_OF_A_KIND
        if vals == [1, 2, 2]:
            return Type.TWO_PAIRS
        if 2 in vals:
            return Type.ONE_PAIR

        return Type.HIGH_CARD

    # These comparisons only apply if they're the same "type"
    def __lt__(self, other: "Hand") -> bool:
        if self.type() == other.type():
            return self.cards < other.cards
        return self.type() < other.type()

    def __eq__(self, other: "Hand") -> bool:
        if self.type() != other.type():
            # unlikely
            return self.cards == other.cards
        return False

    def __str__(self) -> str:
        return "".join([c.Label for c in self.cards])


@dataclass
@total_ordering
class Bid:
    hand: Hand
    bid: int

    def __lt__(self, other: "Bid") -> bool:
        return self.hand < other.hand

    def __eq__(self, other: "Bid") -> bool:
        return self.hand == other.hand

    def __str__(self) -> str:
        return f"{self.hand} {self.bid}"


def part1(filename: str) -> None:
    bids = []
    with open(filename, "r") as f:
        for line in f.readlines():
            labels, bid = line.split()
            bids.append(Bid(Hand([Card(l) for l in labels]), int(bid)))

    bids = sorted(bids)

    print(sum(b.bid * v for v, b in enumerate(bids, 1)))


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
