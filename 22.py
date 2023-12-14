import time
from typing import Dict, List, Tuple
import re
import os


def p1(input: List[str]) -> int:
    return 0

def p2(input: List[str]) -> int:
    return 0

def main():
    with open("in22.txt", "r") as f:
        lines = [l.strip('\n') for l in f.readlines()]
        t1 = time.time()
        print(f"part 1: {p1(lines)}")
        t2 = time.time()
        print(f"part 2: {p2(lines)}")
        t3 = time.time()
        print(f"Part1: {t2-t1} sec")
        print(f"Part2: {t3-t2} sec")

if __name__ == "__main__":
    main()
        