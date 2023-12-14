import time
from typing import Dict, List, Tuple
import re
import os

class Grid:
    lines: List[str]
    width: int
    height: int

    def __init__(self, lines: List[str]):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def print_grid(self, print_reflection_arrows: bool = False):
        for i, l in enumerate(self.lines):
            print(f"{i}: {l}")

    def check_h_reflection(self, idx: int) -> int:
        if idx < 1 or idx > self.width-1:
            raise Exception(f"invalid index: {idx} for h width check")
        # idx is the first to the *right*
        # only allow reflections inside the grid, i.e. 
        # idx \in 1, ..., width-1 
        num_mismatch = 0
        for l in self.lines:
            num_mismatch += self.does_line_match_h(l, idx)
        return num_mismatch

    def check_v_reflection(self, idx: int):
        if idx < 1 or idx > self.height-1:
            raise Exception(f"invalid index: {idx} for h width check")
        # idx is the first to the *right*
        # only allow reflections inside the grid, i.e. 
        # idx \in 1, ..., width-1 
        num_mismatch = 0
        for col in range (0, self.width):
            num_mismatch += self.does_line_match_v(col, idx)
        return num_mismatch

    def does_line_match_h(self, line, idx) -> int:
        n_miss = 0
        for i in range(self.width):
            i_r = idx + i
            i_l = idx - i-1
            if i_l < 0:
                return n_miss
            if i_r >= self.width:
                return n_miss
            if line[i_r] != line[i_l]:
                n_miss += 1
        raise Exception('waaat')

    def does_line_match_v(self, col, idx) -> int:
        n_miss = 0
        for i in range(self.height):
            i_b = idx + i
            i_t = idx - i-1
            if i_t < 0:
                return n_miss
            if i_b >= self.height:
                return n_miss
            if self.lines[i_b][col] != self.lines[i_t][col]:
                n_miss += 1
        raise Exception('wuuut')
            

    def find_reflection(self, target) -> int:
        for idx in range(1, self.width):
            if self.check_h_reflection(idx) == target:
                return idx
        for idx in range(1, self.height):
            if self.check_v_reflection(idx) == target:
                return idx * 100
        raise Exception("found no reflection")



def parse_input(lines: List[str]) -> List[Grid]:
    ret = []
    current_lines = []
    for l in lines:
        if l == "":
            ret.append(Grid(current_lines))
            current_lines = []
        else:
            current_lines.append(l)
    ret.append(Grid(current_lines))
    return ret

def p1(input: List[str]) -> int:
    grids = parse_input(input)
    tot = 0
    for g in grids:
        tot += g.find_reflection(0)
    return tot

def p2(input: List[str]) -> int:
    grids = parse_input(input)
    tot = 0
    for g in grids:
        tot += g.find_reflection(1)
    return tot

def main():
    with open("in13.txt", "r") as f:
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
        