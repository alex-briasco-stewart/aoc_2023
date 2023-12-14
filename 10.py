import time
from typing import Dict, List, Tuple
import re
import os
import sys


#from_dir: 
# 0 = NORTH
# 1 = EAST
# 2 = SOUTH
# 3 = WEST

def reverse_dir(dir: int) -> int:
    return (dir + 2) % 4

def go_to_dir(curr_loc: Tuple[int, int], dir: int) -> Tuple[int, int]:
    if dir == 0:
        return (curr_loc[0]-1, curr_loc[1])
    if dir == 1:
        return (curr_loc[0], curr_loc[1]+1)
    if dir == 2:
        return (curr_loc[0]+1, curr_loc[1])
    if dir == 3:
        return (curr_loc[0], curr_loc[1]-1)
    raise NotImplementedError()

def get_dirs_from_pipe(pipe: str) -> List[int]:
    if pipe == "|":
        return [0, 2]
    elif pipe == "-":
        return [1, 3]
    elif pipe == "L":
        return [0, 1]
    elif pipe == "J":
        return [0, 3]
    elif pipe == "7":
        return [2, 3]
    elif pipe == "F":
        return [1, 2]

    raise NotImplementedError()

def solve_maze(
    maze: Dict[Tuple[int, int], str],
    maze_scores: Dict[Tuple[int, int], int],
    from_dir: int,
    loc: Tuple[int, int],
    from_score: int
):
    curr_score = from_score
    while True:

        if maze[loc] == "S":
            return
        curr_score = curr_score + 1
        if loc in maze_scores and maze_scores[loc] <= curr_score:
            return
        maze_scores[loc] = curr_score

        next_dirs = list(filter(lambda d: d != from_dir, get_dirs_from_pipe(maze[loc])))

        #print(f"{from_dir}, {maze[loc]}, {loc}, {from_score}, {next_dirs}")

        #print(next_dirs)
        assert(len(next_dirs) == 1)
        #solve_maze(maze, maze_scores, reverse_dir(next_dirs[0]), go_to_dir(loc, next_dirs[0]), curr_score)
        from_dir = reverse_dir(next_dirs[0])
        loc = go_to_dir(loc, next_dirs[0])

def solve_maze_2(
    maze: Dict[Tuple[int, int], str],
    maze_scores: Dict[Tuple[int, int], int],
    from_dir: int,
    loc: Tuple[int, int],
    from_score: int
):
    curr_score = from_score
    visited = []
    while True:
        visited.append((loc, from_dir))

        if maze[loc] == "S":
            return visited
        curr_score = curr_score + 1
        if loc in maze_scores and maze_scores[loc] <= curr_score:
            return visited
        maze_scores[loc] = curr_score

        next_dirs = list(filter(lambda d: d != from_dir, get_dirs_from_pipe(maze[loc])))

        #print(f"{from_dir}, {maze[loc]}, {loc}, {from_score}, {next_dirs}")

        #print(next_dirs)
        assert(len(next_dirs) == 1)
        #solve_maze(maze, maze_scores, reverse_dir(next_dirs[0]), go_to_dir(loc, next_dirs[0]), curr_score)
        from_dir = reverse_dir(next_dirs[0])
        loc = go_to_dir(loc, next_dirs[0])


def get_potential_dirs_from_l(pipe, from_dir):
    if pipe == "|":
        if from_dir == 0:
            return [3]
        elif from_dir == 2:
            return [1]
        raise NotImplementedError("bad arg to get_potential_dirs_from_l 1")
    elif pipe == "-":
        if from_dir == 1:
            return [0]
        elif from_dir == 3:
            return [2]
        raise NotImplementedError("bad arg to get_potential_dirs_from_l 2")
    elif pipe == "L":
        if from_dir == 0:
            return [3, 2]
        elif from_dir == 1:
            return []
        raise NotImplementedError("bad arg to get_potential_dirs_from_l 3")
    elif pipe == "J":
        if from_dir == 0:
            return []
        elif from_dir == 3:
            return [1, 2]
        raise NotImplementedError("bad arg to get_potential_dirs_from_l 4")
    elif pipe == "7":
        if from_dir == 3:
            return []
        elif from_dir == 2:
            return [0, 1]
        raise NotImplementedError("bad arg to get_potential_dirs_from_l 5")
    elif pipe == "F":
        if from_dir == 1:
            return [0, 3]
        elif from_dir == 2:
            return []
        raise NotImplementedError("bad arg to get_potential_dirs_from_l 6")
    elif pipe == "S":
        if from_dir == 1:
            return [0]
        elif from_dir == 3:
            return [3]
        else:
            raise NotImplementedError("bad arg to get_potential_dirs_from_l **S**")

    else:
        raise NotImplementedError(f"bad char: {pipe}")



def expand_on_visited(maze: Dict[Tuple[int, int], str], maze_scores: Dict[Tuple[int, int], int], visited: List[Tuple[Tuple[int, int], int]]):
    inside = []
    potential = []
    for l, from_dir in visited:
        new = [go_to_dir(l, d) for d in get_potential_dirs_from_l(maze[l], from_dir)]
        for n in new:
            potential.append(n)
    while True:
        if len(potential) == 0:
            return len(inside)
        l = potential[0]
        potential = potential[1:]
        if l in maze_scores or l in inside:
            continue
        inside.append(l)
        potential.append((l[0]-1, l[1]))
        potential.append((l[0], l[1]-1))
        potential.append((l[0]+1, l[1]))
        potential.append((l[0], l[1]+1))
    


def p1(input: List[str], dirs) -> int:
    maze = {}
    start_idx: Tuple[int, int] | None = None
    for (i, line) in enumerate(input):
        for j, ch in enumerate(line):
            maze[(i, j)] = ch
            if ch == "S":
                start_idx = (i, j)
    if start_idx is None:
        raise NotImplementedError()


    maze_scores = {}
    maze_scores[start_idx] = 0

    # my board start with this:    
    #  --J
    #  -S-
    #  7F-
    #print(maze[start_idx])
    solve_maze(maze, maze_scores, reverse_dir(dirs[0]), go_to_dir(start_idx, dirs[0]), 0)
    solve_maze(maze, maze_scores, reverse_dir(dirs[1]), go_to_dir(start_idx, dirs[1]), 0)
    return max(maze_scores.values())

def p2(input: List[str], dirs) -> int:
    maze = {}
    start_idx: Tuple[int, int] | None = None
    for (i, line) in enumerate(input):
        for j, ch in enumerate(line):
            maze[(i, j)] = ch
            if ch == "S":
                start_idx = (i, j)
    if start_idx is None:
        raise NotImplementedError()


    maze_scores = {}
    maze_scores[start_idx] = 0

    # my board start with this:    
    #  --J
    #  -S-
    #  7F-
    #print(maze[start_idx])


    # need to uncomment one of the below based on if this maze is 'left handed' or 'right handed'
    #visited = solve_maze_2(maze, maze_scores, reverse_dir(dirs[0]), go_to_dir(start_idx, dirs[0]), 0)
    visited = solve_maze_2(maze, maze_scores, reverse_dir(dirs[1]), go_to_dir(start_idx, dirs[1]), 0)
    return expand_on_visited(maze, maze_scores, visited)



def main():
    sys.setrecursionlimit(100000)
    with open("in10.txt", "r") as f:
        # depending on start maze, change this next line [230], and lines 138-142 :/
        dirs = [1, 3]
        lines = [l.strip('\n') for l in f.readlines()]
        t1 = time.time()
        print(f"part 1: {p1(lines, dirs)}")
        t2 = time.time()
        print(f"part 2: {p2(lines, dirs)}")
        t3 = time.time()
        print(f"Part1: {t2-t1} sec")
        print(f"Part2: {t3-t2} sec")

if __name__ == "__main__":
    main()
        