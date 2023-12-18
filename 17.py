import time
from typing import Dict, List, Tuple
import re
import os


def p1(input: List[str]) -> int:
    grid = [
        [int(c) for c in l] for l in input
    ]
    start = (0,0)
    end = (len(grid), len(grid[0]))
    path = astar_search(grid, start, end)
    print(path)
    heat_loss = [grid[p[0]][p[1]] for p in path]
    return heat_loss

def p2(input: List[str]) -> int:
    return 0

def main():
    with open("in17_2.txt", "r") as f:
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
        