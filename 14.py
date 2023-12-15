import time
from typing import Dict, List, Tuple
import re
import os
import functools

@functools.cache
def transpose(lines) -> List[str]:
    out = []
    for _ in range(len(lines[0])):
        out.append("")
    for i in range(len(lines[0])):
        for j in range(len(lines)):
            out[i] += lines[j][i]
    return out


def get_weight_of_line(in_line: str) -> int:
    total_weight = 0
    line_len = len(in_line)
    # scan the line, resetting position to every blocker we see
    roll_idx_start = 0
    num_O_seen = 0
    for idx, ch in enumerate(in_line):
        if roll_idx_start < 0 and ch in "O.":
            roll_idx_start = idx
        if ch == 'O':
            num_O_seen += 1
        elif ch == '#':
            if num_O_seen > 0:
                weight_start = line_len - roll_idx_start
                total_weight += int((weight_start + weight_start - num_O_seen + 1) * num_O_seen / 2)
            num_O_seen = 0
            roll_idx_start = -1
            # we know we're done counting Os for this group.
            # The num_o_seen will end up starting at roll_idx_start
            #weight_start + weight_start - 1 + weight_start -2 + ... + weight_start - num_o_seen-1
    # we hit the end
    if num_O_seen > 0:
        weight_start = line_len - roll_idx_start
        total_weight += int((weight_start + weight_start - num_O_seen + 1) * num_O_seen / 2)
    num_O_seen = 0
    return total_weight

@functools.cache
def tilt_up(in_line: str) -> str:
    line_len = len(in_line)
    # scan the line, resetting position to every blocker we see
    new_line = ''
    roll_idx_start = 0
    num_O_seen = 0
    for idx, ch in enumerate(in_line):
        if roll_idx_start < 0 and ch in "O.":
            roll_idx_start = idx
        if ch == 'O':
            num_O_seen += 1
        elif ch == '#':
            to_add = ('O' * num_O_seen) + ('.' * (idx - roll_idx_start - num_O_seen)) + '#'
            new_line += to_add

            num_O_seen = 0
            roll_idx_start = idx+1
    # we hit the end
    new_line += ('O' * num_O_seen) + ('.' * (line_len - roll_idx_start - num_O_seen))
    num_O_seen = 0
    return new_line

@functools.cache
def rotate_right(lines) -> List[str]:
    # Transpose the rows and columns using zip
    new_lines = []
    line_len = len(lines)
    for _ in range(line_len):
        new_lines.append("")
    for i in range(line_len):
        i_idx = line_len-i-1
        for j in range(len(lines[i_idx])):
            new_lines[j] += lines[i_idx][j]
    return new_lines

@functools.cache
def do_cycle(in_lines: List[str]):
    lines = in_lines
    for _ in range(4):
        lines = transpose(tuple(lines))
        lines = tuple([tilt_up(l) for l in lines])
        lines = tuple(transpose(lines))
        lines = tuple(rotate_right(lines))
    return lines


def p1(input: List[str]) -> int:
    # step 1: transpose the args
    rows = transpose(tuple(input))
    total = sum([get_weight_of_line(r) for r in rows])
    return total
    #print(get_weight_of_line(rows[0]))
    #return 0

def calc_weight(lines) -> int:
    height = len(lines)
    total = 0
    for i, l in enumerate(lines):
        row_sum =  sum([1 if ch=='O' else 0 for ch in l]) * (height - i)
        total += row_sum
    return total


def p2(input: List[str]) -> int:
    lines = input
    for i in range(1000000000):
        lines = do_cycle(tuple(lines))
    tot = calc_weight(lines)

    return tot

def main():
    with open("in14.txt", "r") as f:
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
        