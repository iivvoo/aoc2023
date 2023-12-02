#!/usr/bin/env python3

import sys
import collections


def part1(filename):
    max_red = 12
    max_green = 13
    max_blue = 14

    s = 0
    with open(filename, "r") as f:
        for line in f.readlines():
            grabs = collections.defaultdict(int)

            g, r = line.split(":")
            gid = int(g.split()[-1])

            for rawset in r.split(";"):
                for set in rawset.split(","):
                    set = set.strip()
                    cnt, clr = set.split(" ")
                    cnt = int(cnt)
                    clr = clr.strip()
                    if cnt > grabs[clr]:
                        grabs[clr] = cnt
            if (
                grabs["red"] <= max_red
                and grabs["green"] <= max_green
                and grabs["blue"] <= max_blue
            ):
                s += gid
  

    print(s)


def part2(filename):
    s = 0
    with open(filename, "r") as f:
        for line in f.readlines():
            grabs = collections.defaultdict(int)

            g, r = line.split(":")
            gid = int(g.split()[-1])

            for rawset in r.split(";"):
                for set in rawset.split(","):
                    set = set.strip()
                    cnt, clr = set.split(" ")
                    cnt = int(cnt)
                    clr = clr.strip()
                    if cnt > grabs[clr]:
                        grabs[clr] = cnt

            p = grabs["red"] * grabs["green"] * grabs["blue"]
            s += p
    print(s)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [1|2] <input_file>")
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
