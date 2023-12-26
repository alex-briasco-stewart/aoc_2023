import time
from typing import Dict, List, Tuple
import re
import os
from queue import Queue


def is_valid_move(grid: List[List[str]], pos: Tuple[int, int], max_i, max_j):
    return (pos[0] >= 0 and pos[0] < max_i and pos[1] >= 0 and pos[1] < max_j) and grid[pos[0]][pos[1]] != '#'

def map_grid(grid: List[str], start: Tuple[int, int]):
    # returns map of (i, j) => first able to reach
    max_i = len(grid)
    max_j = len(grid[0])
    reachable = {}
    to_explore = Queue()
    to_explore.put((start, 0))
    while not to_explore.empty():
        pos, step_num = to_explore.get()
        if pos in reachable and reachable[pos] <= step_num:
            # already found a way here cheaper
            continue
        reachable[pos] = step_num
        alternative_positions = [
            (pos[0]+1, pos[1]),
            (pos[0]-1, pos[1]),
            (pos[0], pos[1]+1),
            (pos[0], pos[1]-1),
        ]
        for alt_pos in alternative_positions:
            if is_valid_move(grid, alt_pos, max_i, max_j):
                to_explore.put((alt_pos, step_num+1))
    return reachable

def p1(input: List[str]) -> int:
    start_pos = None
    for i in range(len(input)):
        for j in range(len(input[i])):
            if input[i][j] == "S":
                start_pos = (i, j)
    reachable = map_grid(input, start_pos)
    reachable_in_64 = list(filter(
        lambda k: reachable[k] == 64 or (reachable[k]<64 and reachable[k]%2==0),
        reachable.keys()
    ))
    return len(reachable_in_64)

def solve_2(base, from_top, from_bot, from_left, from_right, n_steps, grid_to_grid_distance):
    if n_steps < grid_to_grid_distance:
        raise Exception("just use the normal one dummy")
    # on-axis need to come from the center direction
    # anything else we can use the optimized ones
    # find the number of complete grids we can reach

    num_complete_grids = (n_steps - 65) % grid_to_grid_distance


def assemble_grid(copies_to_add: int, grid: List[str]):
    new_grid = []
    n = copies_to_add*2+1
    for _ in range(n):
        for i in range(len(grid)):
            new_grid.append(grid[i] * n)
    p = ((len(new_grid)-1) // 2)
    assert(new_grid[p][p] == "S")
    return new_grid, (p, p)

def p2(input: List[str]) -> int:
    #n_steps = (26501365 - 65) // 131
    n_steps = 202300
    a = 14696
    b = 14836
    c = 3738

    return a* (n_steps**2) + b * (n_steps) + c
    #start_pos = None
    #for i in range(len(input)):
    #    for j in range(len(input[i])):
    #        if input[i][j] == "S":
    #            start_pos = (i, j)


    ## steps to try 
    #steps_to_try = []
    #for i in range(15):
    #    steps_to_try.append(65 + 131*i*2)

    #for s in steps_to_try:
    #    copies =(s // 130)*2 + 2
    #    g, pos = assemble_grid(copies, input)
    #    reachable = map_grid(g, pos)
    #    reachable_in_steps = list(filter(
    #        lambda k: reachable[k] == s or (reachable[k]<s and reachable[k]%2==1),
    #        reachable.keys()
    #    ))
    #    print(s, ": ", len(reachable_in_steps))

    ##triple_input = [l+l+l for l in input]
    #reachable = map_grid(input, start_pos)
    #max_i = len(input)
    #max_j = len(input[0])
    #print(max_i, max_j)

    #reachable_from_top = map_grid(input, (0, start_pos[1]))
    #reachable_from_bot = map_grid(input, (len(input)-1, start_pos[1]))
    #reachable_from_left = map_grid(input, (start_pos[0], 0))
    #reachable_from_right = map_grid(input, (start_pos[0], len(input[0])-1))

    #from_top_left = map_grid(input, (0, 0))
    #from_top_right = map_grid(input, (0, max_j-1))
    #from_bot_left = map_grid(input, (max_i-1, 0))
    #from_bot_right = map_grid(input, (max_i-1, max_j-1))




def main():
    with open("in21.txt", "r") as f:
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
        