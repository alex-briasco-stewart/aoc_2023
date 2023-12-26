import time
from typing import Dict, List, Tuple
import re
import os
from queue import Queue
from multiprocessing import Pool

class LineSegment:
    start: Tuple[int, int]
    end: Tuple[int, int]
    is_horizontal: bool
    direction: str

    def __init__(self, start, end, direction):
        self.start = start
        self.end = end
        self.is_horizontal = self.end[0] == self.start[0]
        self.direction = direction
        if not self.is_horizontal:
            assert(self.start[1] == self.end[1])

    def __repr__(self):
        return f"{self.direction}: {self.start} -> {self.end}"

    def get_j_intersection_values(self, i_val) -> List[int]:
        if self.is_horizontal and i_val == self.start[0]:
            return [self.start[1], self.end[1]]
        elif (self.start[0] <= i_val and self.end[0] >= i_val) or (self.end[0]<= i_val and self.start[0] >= i_val):
            return [self.start[1]] # j values should be the same
        else:
            return []
    def is_other_point_inside(self, pnt):
        assert(self.is_horizontal)
        return pnt[0] == self.start[0] and pnt[1] >= min(self.start[1], self.end[1]) and pnt[1] <= max(self.start[1], self.end[1])

def solve_2(min_i, max_i, segments: List[LineSegment]):
    # doesn't work... n_ints % 2 != 0 sometimes
    overall_dug = 0
    for i_val in range(min_i, max_i+1):
        intersections = []
        for seg in segments:
            intersections += seg.get_j_intersection_values(i_val)

        ints = sorted(intersections)
        n_ints = len(ints)
        assert(n_ints%2==0)
        # go through by pairs, plus count numebr of doubles
        vals = {}
        line_total = 0
        for i in range(n_ints // 2):
            i1 = i*2
            i2 = i*2+1

            # count the numebr of doubles
            v1 = ints[i1]
            v2 = ints[i2]
            if v1 in vals:
                vals[v1] += 1
            else:
                vals[v1] = 1
            if v2 in vals:
                vals[v2] += 1
            else:
                vals[v2] = 1
            line_total += v2 - v1 + 1
        n_doubles = sum([1 if v==2 else 0 for v in vals.values()])
        line_total -= n_doubles
        overall_dug += line_total
    return overall_dug

def count_line(segments: List[LineSegment], i_val: int):
    debug = False
    #if i_val == 56407:
    #    debug = True

    intersections = {}
    for s in segments:
        ints = s.get_j_intersection_values(i_val)
        for i in ints:
            if i in intersections:
                intersections[i].append(s)
            else:
                intersections[i] = [s]
    ints_in_order = sorted(intersections.keys())
    total_inside = 0

    inside = False
    last_j_val = -1
    skipnext = False

    for idx, j in enumerate(ints_in_order):
        if debug:
            print(f"for intersection at {j}, inside={inside}")
        if skipnext:
            skipnext = False
            continue
        if len(intersections[j]) == 1:
            if inside:
                # we were inside, now outside
                assert(last_j_val >=0)
                total_inside += j - last_j_val + 1
                last_j_val = -1
            else:
                last_j_val = j
            inside = not inside
        else:
            skipnext = True
            # this is a double intersection and we're inside, add up until the start
            if inside:
                total_inside += j-last_j_val # not plus one, we'll do that later
            next_int = ints_in_order[idx+1]

            total_inside += next_int - j + 1

            int1_dirs = "".join([s.direction for s in intersections[j]])
            int2_dirs = "".join([s.direction for s in intersections[next_int]])
            if (debug):
                print(f"int1_dirs: {int1_dirs}")
                print(f"int2_dirs: {int2_dirs}")
            if ("U" in int1_dirs and "U" in int2_dirs) or ("D" in int1_dirs and "D" in int2_dirs):
                # we swap inside-ness
                if inside:
                    last_j_val = -1
                else:
                    last_j_val = next_int+1
                inside = not inside
            else: # we keep the same inside-ness
                if inside:
                    last_j_val = next_int+1
                else:
                    last_j_val = -1
    if (inside):
        for i in ints_in_order:
            print(f"{i}: {intersections[i]}")
    assert(not inside)
    return total_inside

def solve_2_attempt_2(segments: List[LineSegment], min_i, max_i):
    total_inside = 0
    for i_val in range(min_i, max_i+1):
        #pct = int((100*i_val / (max_i+1 - min_i)))
        #if (pct%10==0):
        #    print(f"{pct/100}")
        total_inside += count_line(segments, i_val)
    return total_inside


    

def parse_input(inp: List[str]) -> List[Tuple[str, int, str]]:
    data = []
    for l in inp:
        m = re.match(r"^([UDLR]) ([\d]+) \((#[a-f0-9]+)\)$", l)
        if m:
            data.append((m.group(1), int(m.group(2)), m.group(3)))
        else:
            raise Exception('failed to match')
    return data
def parse_input_2(inp: List[str]) -> List[Tuple[str, int, str]]:
    data = []
    match_dict = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }
    for l in inp:
        m = re.match(r"^([UDLR]) ([\d]+) \(#([a-f0-9]+)\)$", l)
        if m:
            hex_num = m.group(3)
            dist = int(hex_num[:-1], 16)
            dir = match_dict[hex_num[-1]]
            data.append((dir, dist))
        else:
            raise Exception('failed to match')
    return data


def flood_fill(dug: Dict[Tuple[int, int], str], pos, max_i, max_j, min_i, min_j):
    to_search = Queue()
    to_search.put(pos)
    if pos in dug:
        return
    to_add = {}
    while not to_search.empty() > 0:
        p = to_search.get()
        if p in to_add or p in dug:
            continue
        if p[0] == max_i or p[0] == min_i or p[1] == min_j or p[1] == max_j:
            # we've hit the edge, we want none of these.
            return
        to_add[p] = True
        p1 = (p[0], p[1]+1)
        p2 = (p[0], p[1]-1)
        p3 = (p[0]+1, p[1])
        p4 = (p[0]-1, p[1])
        for _p in [p1, p2, p3, p4]:
            if _p not in to_add and _p not in dug:
                to_search.put(_p)
    # we need to add all of these
    for p in to_add:
        dug[p] = "ADDED"


def p1(input: List[str]) -> int:
    return
    instructions = parse_input(input)
    # remember all the locations we dig. For the grid of (min, min) => (max, max)
    # do flood fill until we hit an edge or until we exhaust the size, then that's the dig amnt
    dug = {}
    i = 0
    j = 0
    max_i = 0
    max_j = 0
    min_i = 0
    min_j = 0
    dug[(i, j)] = "000000"
    for dir, amnt, color in instructions:
        for _ in range(amnt):
            if dir == "U":
                i -= 1
            elif dir == "D":
                i += 1
            elif dir == "L":
                j -= 1
            elif dir == "R":
                j += 1
            dug[(i, j)] = color
            if i > max_i:
                max_i = i
            if i < min_i:
                min_i = i
            if j < min_j:
                min_j = j
            if j > max_j:
                max_j = j
    max_i = max_i + 1
    max_j = max_j + 1
    min_i = min_i - 1
    min_j = min_j - 1


    original_keys = list(dug.keys())
    n_keys = len(original_keys)
    for i, og_key in enumerate(original_keys):
        t = (og_key[0]-1, og_key[1])
        b = (og_key[0]+1, og_key[1])
        r = (og_key[0], og_key[1]-1)
        l = (og_key[0], og_key[1]+1)
        for p in [t, b, r, l]:
            flood_fill(dug, p, max_i, max_j, min_i, min_j)

    #flood_fill(dug, (i, j), max_i, max_j, min_i, min_j)
    return len(list(dug.keys()))

def s2a2_wrapper(tup):
    segs = tup[0]
    min_i = tup[1]
    max_i = tup[2]
    return solve_2_attempt_2(segs, min_i, max_i)

def p2(input: List[str]) -> int:
    instructions = parse_input_2(input)
    min_i = 0
    max_i = 0
    p = (0, 0)
    dirs = {
        "R": (0, 1),
        "L": (0, -1),
        "U": (-1, 0),
        "D": (1, 0),
    }
    segments = []
    for direction, dist in instructions:
        vec = dirs[direction]
        next_p = (p[0] + dist * vec[0], p[1] + dist * vec[1])
        if next_p[0] < min_i:
            min_i = next_p[0]
        if next_p[0] > max_i:
            max_i = next_p[0]
        segments.append(LineSegment(p, next_p, direction))
        p = next_p


    pool_size = 20
    step_size = (max_i - min_i) // pool_size

    args = [(segments, step_size*i + min_i, min_i + step_size*(i+1) - 1) for i in range(pool_size-1)]
    args.append((segments, step_size*(pool_size-1) + min_i, max_i))

    with Pool(pool_size) as p:
        results = p.map(
            s2a2_wrapper,
            args
        )
        return sum(results)

def main():
    with open("in18.txt", "r") as f:
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
        