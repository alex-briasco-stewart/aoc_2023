import time
from typing import Dict, List, Tuple
import re
import os

class GridPoint:
    ch: str
    light_directions: List[bool]
    def __init__(self, _ch):
        self.ch = _ch
        self.light_directions = [False, False, False, False] # COMING FROM (left, top, right, bottom)
    
    def simulate(self):
        # 0 = FROM LEFT
        # 1 = FROM TOP
        # 2 = FROM RIGHT
        # 3 = FROM BOTTOM

        # return the directions that light goes
        if self.ch == ".":
            return [self.light_directions[2], self.light_directions[3], self.light_directions[0], self.light_directions[1]]
        if self.ch == "/":
            return [self.light_directions[1], self.light_directions[0], self.light_directions[3], self.light_directions[2]]
        if self.ch == "\\":
            return [self.light_directions[3], self.light_directions[2], self.light_directions[1], self.light_directions[0]]
        if self.ch == "-":
            return [
                self.light_directions[2] or self.light_directions[1] or self.light_directions[3],
                False,
                self.light_directions[0] or self.light_directions[1] or self.light_directions[3],
                False
            ]
        if self.ch == "|":
            return [
                False,
                self.light_directions[3] or self.light_directions[0] or self.light_directions[2],
                False,
                self.light_directions[1] or self.light_directions[0] or self.light_directions[2]
            ]
        raise Exception("shouldnt happen")


def simulate_grid(grid: List[List[GridPoint]]):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            left, top, right, bottom = grid[i][j].simulate()
            #print(f"({i}, {j}) illuminates (left={left}, right={right}, top={top}, bottom={bottom})")
            if left and j > 0:
                grid[i][j-1].light_directions[2] = True
            if right and j+1 < len(grid[i]):
                grid[i][j+1].light_directions[0] = True
            if top and i > 0:
                grid[i-1][j].light_directions[3] = True
            if bottom and i+1 < len(grid):
                grid[i+1][j].light_directions[1] = True
    score = sum([ 
         sum([1 if any(g.light_directions) else 0 for g in g_line]) for g_line in grid
         ])
    return score

def print_grid(grid: List[List[GridPoint]]):
    for l in grid:
        st = ["#" if any(g.light_directions) else "." for g in l]
        print("".join(st))


def p1(input: List[str]) -> int:
    grid = []
    for l in input:
        g_line = []
        for c in l:
            g_line.append(GridPoint(c))
        grid.append(g_line)
    # initial
    grid[0][0].light_directions[0] = True
    score = -1
    for i in range(100000):
        next_score = simulate_grid(grid)
        if score == next_score:
            for _ in range(10):
                next_score = simulate_grid(grid)
            if next_score == score:
                return score
        else:
            score = next_score

def simulate_p2(input_lines: List[str], init_spot: Tuple[int, int], init_dir: int):
    grid = []
    for l in input_lines:
        g_line = []
        for c in l:
            g_line.append(GridPoint(c))
        grid.append(g_line)
    # initial
    grid[init_spot[0]][init_spot[1]].light_directions[init_dir] = True
    score = -1
    for i in range(100000):
        next_score = simulate_grid(grid)
        if score == next_score:
            for _ in range(10):
                next_score = simulate_grid(grid)
            if next_score == score:
                return score
        else:
            score = next_score

def p2(input: List[str]) -> int:
    scores = []
    for col in range(len(input[0])):
        start_pos_top = (0, col)
        scores.append(simulate_p2(input, start_pos_top, 1))
        start_pos_bot = (len(input) - 1, col)
        scores.append(simulate_p2(input, start_pos_bot, 3))
    for row in range(len(input)):
        start_pos_left = (row, 0)
        start_pos_right = (row, len(input[0])-1)
        scores.append(simulate_p2(input, start_pos_left, 0))
        scores.append(simulate_p2(input, start_pos_right, 2))
    return max(scores)
    

def main():
    with open("in16.txt", "r") as f:
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
        