#!/usr/bin/env python3

import sys
import re

class Engine:
    def __init__(self):
        self.matrix = []

    def read(self, filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                self.matrix.append(list(line.strip()))

    def collect(self):
        numbers = []
        machineparts = []

        for i, row in enumerate(self.matrix):
            parts = re.findall(r'([^\d]{1,}|\d+)', "".join(row))
            offset = 0
            for p in parts:
                if p[0].isdigit():
                    numbers.append((i, offset, p))
                offset += len(p)
            for j, col in enumerate(row):
                if not col.isdigit() and col != ".":
                    machineparts.append((i, j, col))
        return numbers, machineparts 

    def __str__(self):
        return "\n".join("".join(c for c in row) for row in self.matrix)

def part1(filename):
    e = Engine()
    e.read(filename)

    numbers, machineparts = e.collect() 

    s = 0
    def near(nr, nc, nv):
        for pr, pc, pl in machineparts:
            if abs(pr - nr) <= 1:
                # start on or 1 after
                if 0 <= nc - pc <= 1:
                    return True
                # end on or 1 before
                if 0 <= pc - (nc + len(nv) - 1) <= 1:
                    return True
                # overlap
                if nc <= pc <= nc + len(nv) - 1:
                    return True

        return False

    for nr, nc, nv in numbers:
        if not near(nr, nc, nv):
            print("Not:", nv)
        else:
            s += int(nv)

    print(s)

def part2(filename):
    e = Engine()
    e.read(filename)

    numbers, machineparts = e.collect() 

    def near2(pr, pc, pt):
        nearby = []
        for nr, nc, nv in numbers:
            if abs(pr - nr) <= 1:
                # start on or 1 after
                if 0 <= nc - pc <= 1:
                    nearby.append(int(nv))
                    continue
                # end on or 1 before
                if 0 <= pc - (nc + len(nv) - 1) <= 1:
                    nearby.append(int(nv))
                    continue
                # overlap
                if nc <= pc <= nc + len(nv) - 1:
                    nearby.append(int(nv))
                    continue
        if len(nearby) == 2:
            return nearby[0] * nearby[1]
        return 0

    s = 0

    for pr, pc, pt in machineparts:
        if pt != "*":
            continue

        if v := near2(pr, pc, pt):
            s += v

    print(s)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: python {sys.argv[0]} [1|2] <input_file>')
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
