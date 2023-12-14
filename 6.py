from sre_compile import dis
from typing import Dict, List, Tuple
import re
import os
import math

def get_ways_to_win_race(t: int, dist: int):
    speeds = list(range(t+1)) # [0, ..., t]
    distances_travelled = [ s * (t-s) for s in speeds]
    return sum([1 if d > dist else 0 for d in distances_travelled])

def p1(input: List[str]) -> int:
    times = [int(t.strip()) for t in filter(lambda x: len(x) > 0, input[0].split("Time:")[1].strip().split(" "))]
    distances = [int(t.strip()) for t in filter(lambda x: len(x) > 0, input[1].split("Distance:")[1].strip().split(" "))]
    product = 1
    ways_to_win = [get_ways_to_win_race(t, d) for t, d in zip(times, distances)]
    for w in ways_to_win:
        product *= w 

    return product

def p2(input: List[str]) -> int:
    time = int(input[0].split("Time:")[1].strip().replace(" ", ''))
    distance = int(input[1].split("Distance:")[1].strip().replace(" ", ''))

    # just solve the equation lmao
    # distance_travelled = -x^2 + xt, where x is the number of ms held
    # however, we're interested in knowing the values of where we are equal
    # the function that describes our *lead* over the record is f - record, or -x^2 + xt - record
    # in the language of the quadratic formula,
    # a = -1
    # b = t
    # c = -record
    # the zeros of this function will be at:

    #x0 = (-t + sqrt(t^2 - (4 * -1 * -record))) / (-2)
    #x1 = (-t - sqrt(t^2 - (4 * -1 * -record))) / (-2)
    t = time
    record = distance
    x0 = ((-1.0 * t) + math.sqrt(t**2 - (4 * -1 * (-1.0 * record)))) / (-2)
    x1 = ((-1.0 * t) - math.sqrt(t**2 - (4 * -1 * (-1.0 * record)))) / (-2)

    # we want to ceil both of these because the function is not truly quadratic,
    # the real function is equal at each integral value to the quadratic, but is essentially
    # F(x) = f(x0) \forall x \in [x0, x0+1] \forall x0 \in N
    # Put another way, in each interval between two integers, the function takes on the function value at the left-hand side
    # which grants us an additional 1 way to beat the record
    return math.ceil(max([x0, x1])) - math.ceil(min([x0, x1]))

def main():
    with open("in6.txt", "r") as f:
        lines = [l.strip('\n') for l in f.readlines()]
        print(f"part 1: {p1(lines)}")
        print(f"part 2: {p2(lines)}")

if __name__ == "__main__":
    main()
        