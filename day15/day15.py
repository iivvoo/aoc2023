#!/usr/bin/env python3

import sys


class Box:
    def __init__(self, no: int):
        self.no = no
        self.lenses: dict[bytes, int] = {}

    def add(self, label: bytes, lens: int) -> None:
        self.lenses[label] = lens

    def remove(self, label: bytes) -> None:
        try:
            del self.lenses[label]
        except KeyError:
            pass

    def focuspower(self) -> int:
        return sum(
            (self.no + 1) * (pos * focal)
            for pos, focal in enumerate(self.lenses.values(), 1)
        )


def hash(s: bytes) -> int:
    v = 0
    for c in s:
        v += c
        v *= 17
        v %= 256
    return v


def part1(filename: str) -> None:
    input = open(filename, "rb").readline().strip()
    parts = input.split(b",")

    print(sum(hash(p) for p in parts))


def part2(filename: str) -> None:
    input = open(filename, "rb").readline().strip()
    parts = input.split(b",")

    boxes = [Box(i) for i in range(256)]

    for p in parts:
        if b"-" in p:
            label = p[:-1]
            boxes[hash(label)].remove(label)
        else:
            label, lens = p.split(b"=")
            boxes[hash(label)].add(label, int(lens))

    print(sum(b.focuspower() for b in boxes))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
