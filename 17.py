import time
from typing import Dict, List, Tuple
import re
import os
import heapq

def is_in_grid(i, j, grid_len, grid_zero_len):
    return i >= 0 and i < grid_len and j >= 0 and j < grid_zero_len

def search_1(grid: List[List[int]]):
    grid_len = len(grid)
    grid_zero_len = len(grid[0])
    goal = (grid_len-1, grid_zero_len-1)

    heap = []

    # tuple is (*score*, pos=(i,j), movements)
    heapq.heappush(heap, (0, (0, 0), []))
    expanded = {}
    while True:
        score, pos, mvmts = heapq.heappop(heap)
        last_three = "".join(mvmts[-3:])
        if (pos, last_three) in expanded:
            continue
        expanded[(pos, last_three)] = True
        if pos == goal:
            #print_path(grid, mvmts)
            return score
        
        north = (pos[0]-1, pos[1])
        east = (pos[0], pos[1]+1)
        south = (pos[0]+1, pos[1])
        west = (pos[0], pos[1]-1)
        moves = [
            (north, "N"),
            (east, "E"),
            (south, "S"),
            (west, "W"),
        ]
        opposite = {
            "W": "E",
            "E": "W",
            "N": "S", 
            "S": "N"
        }
        for newpos, dir in moves:
            if len(mvmts)>0 and dir == opposite[mvmts[-1]]:
                continue
            if is_in_grid(newpos[0], newpos[1], grid_len, grid_zero_len) and last_three != dir*3:
                heapq.heappush(heap, (score + grid[newpos[0]][newpos[1]], newpos, mvmts + [dir]))

def print_path(grid, path):
    pos = (0, 0)
    visited = []
    print(path)
    for p in path:
        if p == "N":
            pos = (pos[0]-1, pos[1])
        elif p == "S":
            pos = (pos[0]+1, pos[1])
        elif p == "W":
            pos = (pos[0], pos[1]-1)
        elif p == "E":
            pos = (pos[0], pos[1]+1)
        
        visited.append(pos)
    print(visited)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in visited:
                print("#", end="")
            else:
                print(grid[i][j], end='')
        print()


def gen_moves(grid, direction, pos):
    #returns (score_delta, pos, mvmt_delta)
    offset = None
    if direction == "N":
        offset = (-1, 0)
    elif direction == "E":
        offset = (0, 1)
    elif direction == "W":
        offset = (0, -1)
    elif direction == "S":
        offset = (1, 0)
    moves = []
    running_score = 0
    mvmt = []
    grid_len = len(grid)
    grid_zero_len = len(grid[0])
    for i in range(1, 4):
        y = pos[0] + offset[0]*i
        x = pos[1] + offset[1]*i
        if is_in_grid(y, x, grid_len, grid_zero_len):
            running_score += grid[y][x]
            mvmt += [direction]
    for i in range(4, 11):
        newpos = (pos[0] + offset[0]*i, pos[1]+offset[1]*i)
        if is_in_grid(newpos[0], newpos[1], grid_len, grid_zero_len):
            running_score += grid[newpos[0]][newpos[1]]
            moves.append((running_score, newpos, mvmt + [direction]))
            mvmt += [direction]
    return moves

def search_2(grid: List[List[int]]):
    grid_len = len(grid)
    grid_zero_len = len(grid[0])
    goal = (grid_len-1, grid_zero_len-1)

    heap = []

    # tuple is (*score*, pos=(i,j), movements)
    for dscore, init_pos, dmoves in gen_moves(grid, "E", (0, 0)):
        heapq.heappush(heap, (dscore, init_pos, dmoves))
    for dscore, init_pos, dmoves in gen_moves(grid, "S", (0, 0)):
        heapq.heappush(heap, (dscore, init_pos, dmoves))
    expanded = {}
    opposite = {
        "W": "E",
        "E": "W",
        "N": "S", 
        "S": "N"
    }
    while True:
        score, pos, mvmts = heapq.heappop(heap)
        last_ten = "".join(mvmts[-10:])

        if (pos, last_ten) in expanded:
            continue

        expanded[(pos, last_ten)] = True
        if pos == goal:
            #print_path(grid, mvmts)
            return score

        moves = []

        # every time we pop, we are at a location we *must* turn.
        # for each direciton, add: all between 4 and 10 paths, unless 

        for direction in ["N", "S", "E", "W"]:
            if len(mvmts) > 0 and mvmts[-1] == direction or mvmts[-1] == opposite[direction]:
                continue
            moves += gen_moves(grid, direction, pos)

        for dscore, newpos, dmoves in moves:
            if is_in_grid(newpos[0], newpos[1], grid_len, grid_zero_len):
                new = (score + dscore, newpos, mvmts + dmoves)
                heapq.heappush(heap, new)


def p1(input: List[str]) -> int:
    grid = [
        [int(c) for c in l] for l in input
    ]
    return search_1(grid)

def p2(input: List[str]) -> int:
    grid = [
        [int(c) for c in l] for l in input
    ]
    return search_2(grid)

def main():
    with open("in17.txt", "r") as f:
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
        