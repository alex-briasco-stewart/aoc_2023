import time
from typing import Dict, List, Tuple
import re
import os


# returns the next number in the list
def solve_1(nums: List[int]) -> int:
    if all([n == 0 for n in nums]):
        return 0
    else:
        new_nums = []
        for i in range(len(nums) - 1):
            new_nums.append(nums[i+1] - nums[i])
        return nums[-1] + solve_1(new_nums)

# returns the next number in the list
def solve_2(nums: List[int]) -> int:
    if all([n == 0 for n in nums]):
        return 0
    else:
        new_nums = []
        for i in range(len(nums) - 1):
            new_nums.append(nums[i+1] - nums[i])
        nex_n = nums[-1] + solve_2(new_nums)
        return nex_n

def p1(input: List[str]) -> int:
    total = 0
    for line in input:
        total += solve_1([int(n) for n in line.split(" ")])
    return total


def p2(input: List[str]) -> int:
    total = 0
    for line in input:
        nums = [int(n) for n in line.split(" ")]
        nums.reverse()
        total += solve_2(nums)
    return total

def main():
    with open("in9.txt", "r") as f:
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
        