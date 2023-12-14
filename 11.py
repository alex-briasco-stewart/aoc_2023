import time
from typing import Dict, List, Tuple
import re
import os

def transpose(l1):
    l2 = []
    # iterate over list l1 to the length of an item 
    for i in range(len(l1[0])):
        # print(i)
        row =[]
        for item in l1:
            # appending to new list with values and index positions
            # i contains index position and item contains values
            row.append(item[i])
        l2.append(row)
    return l2

def expand_universe(universe: List[str]):
    u2 = []
    for l in universe:
        if all([c == '.' for c in l]):
            u2.append(l)
        u2.append(l)
    u3 = transpose(u2)
    u4 = []
    for l in u3:
        if all([c == '.' for c in l]):
            u4.append(l)
        u4.append(l)
    return transpose(u4)
def expand_universe_pt2(universe: List[str]):
    u2 = []
    for l in universe:
        if all([c in ".n" for c in l]):
            u2.append(["n" for _ in range(len(l))])
        else:
            u2.append(l)

    u3 = transpose(u2)
    u4 = []

    for l in u3:
        if all([c in '.n' for c in l]):
            u4.append(["n" for _ in range(len(l))])
        else:
            u4.append(l)
    return transpose(u4)

def get_galaxy_locations(u: List[List[str]]):
    locs = []
    for i in range(len(u)):
        for j in range(len(u[i])):
            if u[i][j]=="#":
                locs.append((i, j))
    return locs

def generate_powerset(items):
    vals = []
    for (idx, i1) in enumerate(items):
        for i2 in items[idx+1:]:
            vals.append((i1, i2))
    return vals
def distance_between(g1: Tuple[int, int], g2: Tuple[int, int]):
    return abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])

def distance_between_p2(g1: Tuple[int, int], g2: Tuple[int, int], u: List[List[str]], multiplier: int):
    # start at g1, walk to g2 along x then y, count number of n-s
    distance = 0
    num_n = 0
    xdir = 1 if g2[0] > g1[0] else -1
    ydir = 1 if g2[1] > g1[1] else -1
    for x in range(g1[0]+xdir, g2[0]+xdir, xdir): # +xdir to make range exclusive at start, inclusive at end
        if u[x][g1[1]] == 'n':
            num_n += 1
        else:
            distance += 1
    for y in range(g1[1]+ydir, g2[1]+ydir, ydir):
        if u[g2[0]][y] == 'n':
            num_n += 1
        else:
            distance += 1
    return distance + num_n * multiplier


def p1(input: List[str]) -> int:
    return sum([distance_between(g1, g2) for g1, g2 in generate_powerset(get_galaxy_locations(expand_universe(input)))])

def p2(input: List[str]) -> int:
    multiplier = int(1e6)
    u = expand_universe_pt2(input)
    return sum([distance_between_p2(g1, g2, u, multiplier) for g1, g2 in generate_powerset(get_galaxy_locations(u))])

def main():
    with open("in11.txt", "r") as f:
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
        