import time
from typing import Dict, List, Tuple
import re
import math
import os

class Hailstone:
    pos: Tuple[int, int, int]
    vel: Tuple[int, int, int]
    def __init__(self, in_line: str):
        m = re.match(r"([\-0-9]+),\s+([\-0-9]+),\s+([\-0-9]+)\s+@\s+([\-0-9]+),\s+([\-0-9]+),\s+([\-0-9]+)", in_line)
        if m is None:
            raise Exception("failed to parse")
        self.pos = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        self.vel = (int(m.group(4)), int(m.group(5)), int(m.group(6)))
    
    def get_general_form(self):
        m = self.vel[1] / self.vel[0]
        a1 = -1.0 * m
        b1 = 1
        c1 = self.pos[1] - m * self.pos[0]
        return a1, b1, c1

    def get_slope(self):
        return self.vel[1] / self.vel[0]

    def get_intersection_point_p1(self, other):
        if abs(self.get_slope() - other.get_slope()) < 1e-7:
            return None, None, None
        a1, b1, c1 = self.get_general_form()
        a2, b2, c2 = other.get_general_form()
        x_val = (c1*b2 - b1*c2) / (a1*b2-b1*a2)
        y_val = (a1*c2-c1*a2) / (a1*b2-b1*a2)

        t1 = (x_val - self.pos[0]) / self.vel[0]
        t2 = (x_val - other.pos[0]) / other.vel[0]
        return (x_val, y_val), t1, t2


def p1(input: List[str]) -> int:
    hailstones = [Hailstone(l) for l in input]
    min_p = 200000000000000
    max_p = 400000000000000
    #min_p = 7
    #max_p = 27
    n_ints = 0
    for i in range(len(hailstones)):
        for j in range(i+1, len(hailstones)):
            int_pos, t1, t2 = hailstones[i].get_intersection_point_p1(hailstones[j])
            if int_pos is not None and t1 > 0 and t2 > 0:
                if int_pos[0] >= min_p and int_pos[0] <= max_p and int_pos[1] >= min_p and int_pos[1] <= max_p:
                    n_ints += 1
    return n_ints

def p2(input: List[str]) -> int:
    return 0

def main():
    with open("in24.txt", "r") as f:
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
        