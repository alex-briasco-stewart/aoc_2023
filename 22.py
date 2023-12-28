import time
from typing import Dict, List, Tuple
import re
import os
from queue import Queue


class Brick:
    min_pos: Tuple[int, int, int]
    max_pos: Tuple[int, int, int]
    supports: List[int]
    supported_by: List[int]
    top_blocks: List[Tuple[int, int, int]]
    idx: int

    def __init__(self, in_str):
        m = re.match(r"([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)", in_str)
        if m is None:
            raise Exception("failed to parse")
        self.idx = -1
        self.min_pos = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        self.max_pos = (int(m.group(4)), int(m.group(5)), int(m.group(6)))
        self.supported_by = []
        self.supports = []

        assert(self.max_pos[0] >= self.min_pos[0])
        assert(self.max_pos[1] >= self.min_pos[1])
        assert(self.max_pos[2] >= self.min_pos[2])

    def set_z_level(self, new_z):
        delta = new_z - self.min_pos[2]
        self.min_pos = (self.min_pos[0], self.min_pos[1], self.min_pos[2] + delta)
        self.max_pos = (self.max_pos[0], self.max_pos[1], self.max_pos[2] + delta)
        self.top_blocks = self._calc_top_blocks()

    def is_vertical(self):
        return self.max_pos[2] != self.min_pos[2]

    def _calc_top_blocks(self):
        if self.is_vertical():
            return [self.max_pos]
        if self.max_pos[1] > self.min_pos[1]:
            return [(self.min_pos[0], jval, self.min_pos[2]) for jval in range(self.min_pos[1], self.max_pos[1]+1)]
        elif self.max_pos[0] >= self.min_pos[0]:
            return [(ival, self.min_pos[1], self.min_pos[2]) for ival in range(self.min_pos[0], self.max_pos[0]+1)]
        else:
            raise Exception("unreachable?")


def fall_brick(b: Brick, fallen_bricks: List[Brick]):
    other_bricks = list(filter(lambda t: len(t[1])>0, map(lambda _b: (_b, [bl for bl in _b.top_blocks if bl[0] >= b.min_pos[0] and bl[0] <= b.max_pos[0] and bl[1] >= b.min_pos[1] and bl[1] <= b.max_pos[1]]), fallen_bricks)))
    max_z = 0
    supported_by = []
    for ob, top_blocks in other_bricks:
        assert(len(top_blocks)>0)
        zval = top_blocks[0][2]
        if  zval > max_z:
            max_z = zval
            supported_by = [ob]
        elif zval == max_z:
            supported_by.append(ob)
    
    b.set_z_level(max_z+1)
    b.supported_by = [ob.idx for ob in supported_by]
    for ob in supported_by:
        ob.supports.append(b.idx)

    fallen_bricks.append(b)

def count_num_that_would_fall(bricks: List[Brick], disintegrated: Brick):
    to_check = disintegrated.supports

    fallen = {disintegrated.idx: True}

    while len(to_check)>0:
        idx = to_check[0]
        to_check = to_check[1:]
        if idx in fallen:
            continue
        b = bricks[idx]
        # if all of the bricks in supported_by have fallen, this falls too
        if all([i in fallen for i in b.supported_by]):
            fallen[b.idx] = True
            for bidx in b.supports:
                to_check.append(bidx)
        elif any([i in to_check for i in b.supported_by]):
            to_check.append(idx)
        to_check = sorted(to_check, key=lambda i: bricks[i].min_pos[2])

    return len(fallen.keys()) - 1
    

def get_bricks(input):
    bricks = [Brick(l) for l in input]
    bricks = sorted(bricks, key=lambda b: b.min_pos[2])

    for i, b in enumerate(bricks):
        b.idx = i
    return bricks

def p1(input: List[str]) -> int:
    bricks = get_bricks(input)
    fallen_bricks = []
    for b in bricks:
        # find any bricks that this one will fall down on
        fall_brick(b, fallen_bricks)

    n_can_disintegrate = 0
    for b in fallen_bricks:
        if all([len(bricks[b2_idx].supported_by) >= 2 for b2_idx in b.supports]):
            n_can_disintegrate += 1

    return n_can_disintegrate

def p2(input: List[str]) -> int:
    bricks = get_bricks(input)
    fallen_bricks = []
    for b in bricks:
        # find any bricks that this one will fall down on
        fall_brick(b, fallen_bricks)


    fallen = 0
    for b in bricks:
        fall = count_num_that_would_fall(bricks, b)
        fallen +=  fall
    return fallen

def main():
    with open("in22.txt", "r") as f:
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
        