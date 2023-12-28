import time
from typing import Dict, List, Tuple
import re
import math
import os
import numpy as np
from decimal import Decimal
#from sympy import Matrix
from mpmath import matrix, lu_solve, mp

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
        if abs(self.get_slope() - other.get_slope()) < 1e-6:
            return None, None, None
        a1, b1, c1 = self.get_general_form()
        a2, b2, c2 = other.get_general_form()
        x_val = (c1*b2 - b1*c2) / (a1*b2-b1*a2)
        y_val = (a1*c2-c1*a2) / (a1*b2-b1*a2)

        t1 = (x_val - self.pos[0]) / self.vel[0]
        t2 = (x_val - other.pos[0]) / other.vel[0]
        return (x_val, y_val), t1, t2

    def project_onto_direction(self, dir: Tuple[int, int, int]):
        x = np.array(self.pos, dtype=np.float64)
        v = np.array(self.vel, dtype=np.float64)
        n = np.array(dir, dtype=np.float64)
        n /= np.linalg.norm(n)

        proj_x = x - np.dot(x, n) * n
        proj_v = v - np.dot(v, n) * n
        return tuple(proj_x), tuple(proj_v)

def get_2d_general_form(pos, vel):
    m = vel[1] / vel[0]
    a1 = -1.0 * m
    b1 = 1
    c1 = pos[1] - m * pos[0]
    return a1, b1, c1

def do_lines_intersect_in_3d(l1, l2):
    # check 2d first
    r1, v1 = l1
    r2, v2 = l2
    # solve for intersection in 3d
    # first check xy sloves are not parallel
    if abs(v1[0]) < 1e-7:
        return False, False
    if abs(v2[0]) < 1e-7:
        return False, False

    m1 = v1[1] / v1[0]
    m2 = v2[1] / v2[0]
    if abs(m2-m1) < 1e-6:
        return False, False

    x1, y1, z1 = r1
    x2, y2, z2 = r2

    vx1, vy1, vz1 = v1
    vx2, vy2, vz2 = v2

    if abs(vx1) < 1e-7:
        return False, False
    
    # else, find the lambda and mu params that solve the equation x1 + lambda*v1 = x2+mu*v2
    num = (y1 - y2) + ((vy1*x2)/(vx1)) - ((x1*vy1)/(vx1))
    denom = vy2 - ((vy1*vx2)/(vx1))

    _mu = num / denom
    _lambda = (x2 + _mu*vx2 - x1) / vx1
    #if not abs((_lambda*vx1 + x1) - (_mu*vx2 + x2)) < 1:
    #    print(abs(_lambda*vx1 + x1) - (_mu*vx2 + x2))
    #    exit()
    #if not abs((_lambda*vy1 + y1) - (_mu*vy2 + y2)) < 1:
    #    print(abs((_lambda*vy1 + y1) - (_mu*vy2 + y2)))
    #    exit()

    # check that these equations agree for 
    if ((z1 + _lambda*vz1) - (z2 + _mu * vz2) < 1e-6):
        int_x = x1 + vx1*_lambda
        int_y = y1 + vy1*_lambda
        int_z = z1 + vz1*_lambda
        return True, (int_x, int_y, int_z)

    return False, None



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

def try_direction(direction, hailstones):
    l0 = hailstones[0].project_onto_direction(direction)
    l1 = hailstones[1].project_onto_direction(direction)

    do_intercept, init_pos = do_lines_intersect_in_3d(l0, l1)
    if not do_intercept:
        return False, False

    for idx in range(2, len(hailstones)):
        ln = hailstones[idx].project_onto_direction(direction)
        do_int, int_pos = do_lines_intersect_in_3d(l0, ln)
        if not do_int or \
            abs(int_pos[0] - init_pos[0]) > 1e-6 or \
            abs(int_pos[1] - init_pos[1]) > 1e-6 or \
            abs(int_pos[2] - init_pos[2]) > 1e-6:
            return False, False
    print(f"we match in direction {direction}")
    return True, int_pos

def get_intersection_line(hailstones: List[Hailstone]):
    r = 400
    for i in range(-1 * r, r, 1):
        print(f"i={i}")
        for j in range(-1 * r, r, 1):
            for k in range(-1 * r, r, 1):
                direction = [i, j, k]
                success, int_pos  = try_direction(direction, hailstones)
                if success:
                    return int_pos, direction


def assemble_linear_problem(hailstones): # returns M, b for mx=b
    m = np.ones((4, 4))
    b = np.ones((4, 1))
    h0 = hailstones[0]
    xn = h0.pos[0]
    yn = h0.pos[1]
    vxn = h0.vel[0]
    vyn = h0.vel[1]


    for i, h1 in enumerate(hailstones[1:5]):
        xi = h1.pos[0]
        yi = h1.pos[1]
        vxi = h1.vel[0]
        vyi = h1.vel[1]
        m[i] = [vyn-vyi, vxi-vxn, yi-yn, xn-xi]
        b[i] = xn*vyn - xi*vyi + yi*vxi - yn*vxn
    return m, b

def solve_z(h1, h2, x, vx):
    t1 = (h1.pos[0] - x) / (vx - h1.vel[0])
    t2 = (h2.pos[0] - x) / (vx - h2.vel[0])

    zi = h1.pos[2]
    zj = h2.pos[2]
    vzi = h1.vel[2]
    vzj = h2.vel[2]

    m = matrix([
        [1, t1],
        [1, t2]
    ])
    b = matrix(
        [[zi+t1*vzi], [zj+t2*vzj]]
    )
    print(t1)
    print(t2)
    #return m.solve(b)
    return lu_solve(m, b)



def p2(input: List[str]) -> int:
    np.set_printoptions(precision=15)
    hailstones = [Hailstone(l) for l in input][15:]

    m, b = assemble_linear_problem(hailstones)
    sm = matrix(m.tolist())
    sb = matrix(b.tolist())
    sol = lu_solve(sm, sb)
    print(sol)
    result = solve_z(hailstones[0], hailstones[1], sol[0], sol[2])
    x, y, z = sol[0], sol[1], result[0]
    vx, vy, vz = round(sol[2]), round(sol[3]), round(result[1])

    return int(x + y + z)

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
        