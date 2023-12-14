import time
from typing import Dict, List, Tuple
import re
import os
import math



def parse_maze(maze_lines):
    maze = {}
    for l in maze_lines:
        m = re.match(r"([A-Z1-9]+) = \(([A-Z1-9]+),\s([A-Z1-9]+)\)", l)
        if m is None:
            raise Exception("bad match")
        maze[m.group(1)] = (m.group(2), m.group(3))
    return maze

def find_zzz(input, maze):
    idx = 0
    n_steps = 0
    current = "AAA"
    path = []
    while True:
        path.append(current)

        if current == "ZZZ":
            return n_steps
        if idx == len(input):
            idx -= len(input)
        if input[idx] == "L":
            current = maze[current][0]
        else:
            current = maze[current][1]
        idx += 1
        n_steps += 1

def go_until_node_ends_in_z(dirs, maze, start, start_idx) -> Tuple[str, int]:
    idx = start_idx
    d_len = len(dirs)
    current = start
    while True:
        if dirs[idx % d_len] == "L":
            current = maze[current][0]
        else:
            current = maze[current][1]
        idx += 1
        if current[-1] == "Z":
            return (current, idx)


def p1(input: List[str]) -> int:
    dirs = input[0]
    maze = parse_maze(input[2:])
    return find_zzz(dirs, maze)

def p2(input: List[str]) -> int:
    dirs = input[0]
    maze = parse_maze(input[2:])

    starting_locations: List[str] = [k for k in maze.keys() if k[-1] == "A"]
    tracking: Dict[str, Tuple[str, int]] = {
        s: (s, 0)
        for s in starting_locations
    }
    deltas = {s: [] for s in starting_locations}

    largest_seen = 0
    while True:
        # pick the lowest node
        # move that one until it ends in Z
        k = min(tracking.keys(), key=lambda k: tracking[k][1])
        new = go_until_node_ends_in_z(dirs, maze, tracking[k][0], tracking[k][1])
        if (new[1]-tracking[k][1]) not in deltas[k]:
            deltas[k].append(new[1]-tracking[k][1]) 
        tracking[k] = new
        steps = tracking[k][1]
        if steps > largest_seen + 10e6:
            largest_seen = steps
            print(tracking)# this becomes cyclical after a few steps... run for ~90e6 times and then just solve
            print(deltas)
        if tracking[k][0][-1] == "Z" and all([v[0][-1]=="Z" and v[1]==steps for v in tracking.values()]):
            return steps

def lcm(x, y):
   if x > y:
       greater = x
   else:
       greater = y

   while(True):
       if ((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1

   return lcm

def main():
    with open("in8.txt", "r") as f:
        lines = [l.strip('\n') for l in f.readlines()]
        t1 = time.time()
        print(f"part 1: {p1(lines)}")
        t2 = time.time()
        #print(f"part 2: {p2(lines)}")
        print(f"part 2: {math.lcm(17141, 16579, 18827, 12083, 13207, 22199)}")
        t3 = time.time()
        print(f"Part1: {t2-t1} sec")
        print(f"Part2: {t3-t2} sec")

if __name__ == "__main__":
    main()
        