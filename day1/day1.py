#!/usr/bin/env python3

import sys

def day1_2(filename):
    s = 0
    with open(filename) as f:
        for line in f.readlines():
            digits = ""
            for i, c in enumerate(line):
                if '0' <= c <= '9':
                    digits += c
                else:
                    for j, number in enumerate(("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")):
                        if line[i:].startswith(number):
                            digits += str(j + 1)
                            break
            s += int(digits[0] + digits[-1])
    print(s)


def day1_1(filename):
    s = 0
    with open(filename) as f:
        for line in f.readlines():
            digits = "".join(c for c in line if '0' <= c <= '9')
            s += int(digits[0] + digits[-1])
    print(s)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python day1.py [1|2] <input_file>')
        sys.exit(1)
    if sys.argv[1] == "1":
        day1_1(sys.argv[2])
    else:
        day1_2(sys.argv[2])
