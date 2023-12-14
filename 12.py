import time
from typing import Dict, List, Tuple
import re
import os

def solve_1_recursive(indices: List[List[int]], spring_lengths: List[int]) -> List[List[int]]:
    if len(indices) == 0:
        raise Exception("shouldn't happen")
    if len(indices[0]) == 0:
        raise RuntimeError("no solutions")
    
    if len(indices) == 1:
        return [[i] for i in indices[0]]

    found = []
    for idx in indices[0]:
        # equivalent to choosing `idx` for the zero-th position spring
        last_invalid_index = idx + spring_lengths[0]
        rec_indices = list(map(lambda lst: list(filter(lambda v: v > last_invalid_index, lst)), indices[1:]))
        try:
            remaining = solve_1_recursive(rec_indices, spring_lengths[1:])
            for r in remaining:
                found.append([idx]+r)
        except RuntimeError:
            continue
    return found

def filter_out_springs(in_str, exclusion_ranges):
    # thx chatgpt
    result = ""
    current_index = 0
    for start, length in exclusion_ranges:
        result += in_str[current_index:start]
        current_index = start + length
    result += in_str[current_index:]
    return result

def check_solution(line: str, idxes: List[int], spring_lengths: List[int]):
    exclusion_ranges = list(zip(idxes, spring_lengths))
    return "#" not in filter_out_springs(line, exclusion_ranges)

def solve_row_1(line: str, springs: List[int]) -> int:
    # find valid incides for each spring
    line_len = len(line)
    spring_indices = []
    for idx, s_len in enumerate(springs): # only start looking at indices that are possible... i.e. sum of all prev springs + 1 per spring
        prev_springs = springs[:idx]
        valid_indices = [
            i 
            for i in range(sum(prev_springs) + len(prev_springs), line_len, 1)
            if line_len >= i+s_len and "." not in line[i:i+s_len]
        ]
        spring_indices.append(valid_indices)
    solns = solve_1_recursive(spring_indices, springs)
    tot = 0
    for sol in solns:
        if (check_solution(line, sol, springs)):
            tot += 1
        #else:
        #    print(f"{line} <- {sol} is invalid")
    #p1: print(f"{line} -> {tot}")
    return tot

def solve_2(line: str, springs: List[int], memoized: Dict[Tuple[str, str], int]) -> int:
    #print(f"{line} - {springs}")
    springs_str = hex(sum([s*(16**i) for i, s in enumerate(springs)]))
    key = (line, springs_str)
    if key in memoized:
        return memoized[key]

    line_len = len(line)

    if len(springs) == 0:
        if '#' in line: # placed all the springs but there's a # left
            memoized[key] = 0
            #print(f"  ran out of springs, # left: {line}")
            return 0
        else:
            #print("  ran out of springs")
            memoized[key] = 1
            return 1

    # there's at least one spring left and we have no line left!
    if line_len == 0:
        #print("  ran out of line, no springs")
        memoized[key] = 0
        return 0

    if line_len < sum(springs) + len(springs) - 1:
        #print("  gonna run out of space before placing all springs")
        memoized[key] = 0
        return 0

    tot = 0
    idx = 0
    while True:

        if idx + springs[0] > line_len:
            memoized[key] = tot
            #print(" outta room")
            return tot
        #if this is a valid place to put our spring

        if idx > 0 and line[idx-1] == "#":
            memoized[key] = tot
            #print(" passed a #")
            return tot # we won't be able to place this spring anywhere else

        can_place_here = "." not in line[idx:idx+springs[0]]
        #print('start')
        if can_place_here:
            # check next
            next_idx = idx + springs[0]
            if next_idx < line_len and line[next_idx] == "#":
                idx += 1
                #print("continuing")
                continue

        if can_place_here:
            val = solve_2(line[idx + springs[0] + 1:], springs[1:], memoized)
            #print(f"  trying idx {idx} for {springs[0]} on {line} => {val}")
            tot += val

        #if "." not in line[idx:idx+springs[0]] and ((idx + springs[0] == line_len) or (idx+springs[0] < line_len and line[idx+springs[0] != "#"])):
        #    print(f"  trying idx {idx} for {springs[0]} on {line}")
        #    # we can use this spot

        idx += 1

    
    # line is the remainder of the line
    # springs


def solve_row_2(_line: str, _springs: List[int], memoized: Dict[Tuple[str, str], int]) -> int:
    springs = []
    line = ""
    for _ in range(5):
        line += _line
        springs += _springs
        line += "?"

    line = line[:len(line)-1]

    tot = solve_2(line, springs, memoized)
    #p1: print(f"{line} -> {tot}")
    return tot


def p1(input: List[str]) -> int:
    tot = 0
    for line in input:
        row, springs = line.split(" ")
        springs = [int(s) for s in springs.split(",")]
        tot += solve_row_1(row, springs)
    return tot

def p2(input: List[str]) -> int:
    tot = 0
    memoized = {}
    for line in input:
        row, springs = line.split(" ")
        springs = [int(s) for s in springs.split(",")]
        #val1 = solve_row_1(row, springs)
        val2 = solve_row_2(row, springs, memoized)
        tot += val2
        #if val1 != val2:
        #    print(line)

    
    return tot

def main():
    with open("in12.txt", "r") as f:
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
        