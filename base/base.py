#!/usr/bin/env python3

import sys

def part1(filename):
    pass

def part2(filename):
    pass
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: python {sys.argv[0]} [1|2] <input_file>')
        sys.exit(1)
    if sys.argv[1] == "1":
        part1(sys.argv[2])
    else:
        part2(sys.argv[2])
