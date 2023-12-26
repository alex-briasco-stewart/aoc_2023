import time
from typing import Dict, List, Tuple
import re
import os
from queue import Queue

# dir:
# 1 = up
# 2 = right
# 3 = down
# 4 = left

def is_valid_move(grid, gridsize, new, visited, dir, oldch, skipslopes=False):
    slopes = {
        "^": 1,
        ">": 2,
        "v": 3,
        "<": 4
    }

    if new in visited:
        return False
    if new[0] < 0 or new[1] < 0 or new[0] >= gridsize or new[1] >= gridsize:
        return False

    ch = grid[new[0]][new[1]] 
    if ch == '#':
        return False
    if not skipslopes and (oldch in slopes and slopes[oldch] != dir):
        return False
    return True
    # tuple of (pos, visited)

def find_longest_path(grid: List[str], skipslopes: bool):
    gridsize = len(grid)
    goal = (gridsize-1, gridsize-2)

    active_paths = Queue()
    active_paths.put(((0, 1), {(0, 1): True}))
    maxlen = 0
    it = 0
    while not active_paths.empty():
        it += 1
        if (it%10000 == 0):
            print(f"{it}: {active_paths.qsize()}")
        pos, visited = active_paths.get()
        if pos == goal:
            pathlen = len(visited)
            if maxlen < pathlen:
                maxlen = pathlen
        curr_ch = grid[pos[0]][pos[1]]
        new_moves = [m for m in [
            ((pos[0]+1, pos[1]), 3),
            ((pos[0]-1, pos[1]), 1),
            ((pos[0], pos[1]+1), 2),
            ((pos[0], pos[1]-1), 4)
        ] if is_valid_move(grid, gridsize, m[0], visited, m[1], curr_ch, skipslopes)]
        while len(new_moves) == 1:
            n, d = new_moves[0]

            pos = n
            visited[pos] = True

            curr_ch = grid[pos[0]][pos[1]]

            if pos == goal:
                vlen = len(visited)
                if vlen > maxlen:
                    maxlen = vlen


            new_moves = [m for m in [
                ((pos[0]+1, pos[1]), 3),
                ((pos[0]-1, pos[1]), 1),
                ((pos[0], pos[1]+1), 2),
                ((pos[0], pos[1]-1), 4)
            ] if is_valid_move(grid, gridsize, m[0], visited, m[1], curr_ch, skipslopes)]

        for n, d in new_moves:
            v = visited.copy()
            v[n] = True
            active_paths.put((n, v))
    return maxlen - 1

def find_graph_nodes(grid: List[str]):
    gridsize = len(grid)
    nodes = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }
    nodes = []
    for i in range(gridsize):
        for j in range(gridsize):
            pos = (i, j)
            if grid[i][j] == '#':
                continue
            new_moves = [m[0] for m in [
                ((pos[0]+1, pos[1]), 3),
                ((pos[0]-1, pos[1]), 1),
                ((pos[0], pos[1]+1), 2),
                ((pos[0], pos[1]-1), 4)
            ] if is_valid_move(grid, gridsize, m[0], {}, m[1], '.', True)]
            if len(new_moves) > 2:
                nodes.append(pos)
    return nodes

def get_all_moves_pt2(grid, pos: Tuple[int, int]):
    moves = [m[0] for m in [
        ((pos[0]+1, pos[1]), 3),
        ((pos[0]-1, pos[1]), 1),
        ((pos[0], pos[1]+1), 2),
        ((pos[0], pos[1]-1), 4)
    ] if is_valid_move(grid, len(grid), m[0], {}, m[1], '.', True)]
    return moves

def get_next_node(grid, pos, visited, nodes):
    curr_pos = pos
    it = 0
    while True:
        it += 1
        moves = [m for m in get_all_moves_pt2(grid, curr_pos) if m not in visited]
        if len(moves) == 0:
            return None, None
        if len(moves) != 1:
            assert(curr_pos in nodes)
            return curr_pos, len(visited) - 1
        curr_pos = moves[0] 
        visited.append(curr_pos)

def find_node_connectivity(grid, nodes):
    node_conn = {n: [] for n in nodes}
    for n in nodes:
        for m in get_all_moves_pt2(grid, n):
            # find the node at the end of the path starting with m
            visited = [m, n]
            next_node, dist = get_next_node(grid, m, visited, nodes)
            if next_node is not None:
                node_conn[n].append((next_node, dist))
    return node_conn


def part2_dfs(start_node, end_node, graph, visited):
    if start_node == end_node:
        return 0
    visited[start_node] = True
    max_route = -1
    for n, dist in graph[start_node]:
        if n not in visited or not visited[n]:
            r = part2_dfs(n, end_node, graph, visited)
            if r >= 0:
                d = r + dist
                if d > max_route:
                    max_route = d
    visited[start_node] = False
    return max_route


def p1(input: List[str]) -> int:
    return find_longest_path(input, False)

def p2(input: List[str]) -> int:
    nodes = find_graph_nodes(input)
    node_conn = find_node_connectivity(input, nodes)
    gridsize = len(input)

    start_node = get_next_node(input, (0, 1), [(0, 1)], nodes)
    end_node = get_next_node(input, (gridsize-1, gridsize-2), [(gridsize-1, gridsize-2)], nodes)

    n2n_dist = part2_dfs(start_node[0], end_node[0], node_conn, {start_node[0]: True})

    return start_node[1] + n2n_dist + end_node[1]
    # determine connectivity and cost


def main():
    with open("in23.txt", "r") as f:
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
        