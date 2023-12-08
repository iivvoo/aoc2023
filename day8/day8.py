#!/usr/bin/env python3

import sys
import re
import math

def part1(filename: str) -> None:
    map = {}

    with open(filename, "r") as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f.readlines():
            source, ldir, rdir, _ = re.split("[^A-Z]+", line.strip())
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
    map = {}

    with open(filename, "r") as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f.readlines():
            source, ldir, rdir, _ = re.split(r"[^\w]+", line.strip())
            map[source] = {"L": ldir, "R": rdir}

        starts = [k for k in map.keys() if k[-1] == "A"]
        loops = {}

        for p in starts:
            count = 0
            current = p
            while True:
                for instr in instructions:
                    count += 1
                    current = map[current][instr]
                    if current[-1] == "Z":
                        loops[p] = count
                        break
                if p in loops:
                    break

        print(math.lcm(*loops.values()))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
