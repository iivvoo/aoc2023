#!/usr/bin/env python3

import sys
import re

def part1(filename: str) -> None:
    map = {}

    with open(filename, "r") as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f.readlines():
            source, ldir, rdir, _ = re.split("[^A-Z]+", line.strip())
            print(source, ldir, rdir)
            map[source] = {"L": ldir, "R": rdir}

        current = "AAA"
        count = 0
        while True:
            for instr in instructions:
                count += 1
                current = map[current][instr]
                if current == "ZZZ":
                    print(count)
                    return

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
