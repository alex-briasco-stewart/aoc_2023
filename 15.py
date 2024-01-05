import time
from typing import Dict, List, Tuple
import re
import os

class Box:
    lens_slots: List[Tuple[str, int]]
    box_num: int

    def __init__(self, box_num: int):
        self.lens_slots = []
        self.box_num = box_num
    
    def insert(self, lens_label: str, focal_length: int):
        for i in range(len(self.lens_slots)):
            if self.lens_slots[i][0] == lens_label:
                self.lens_slots[i] = (lens_label, focal_length)
                return
        self.lens_slots.append((lens_label, focal_length))

    def remove(self, lens_label: str):
        for i in range(len(self.lens_slots)):
            if self.lens_slots[i][0] == lens_label:
                self.lens_slots.remove(self.lens_slots[i])
                return
            
    def __repr__(self):
        lens_strings = [f"[{label} {length}]" for label, length in self.lens_slots]
        print(f"Box {self.box_num}: {' '.join(lens_strings)}")

    def get_box_power(self):
        score = 0
        for i, (_, length) in enumerate(self.lens_slots):
            score += (1 + self.box_num) * (i+1) * length
        return score

def hash(in_str: str):
    score = 0
    for ch in in_str:
        score = ((score + ord(ch)) * 17) % 256
    return score

def p1(input: List[str]) -> int:
    in_line = input[0]
    return sum([hash(seq) for seq in in_line.split(",")])

def p2(input: List[str]) -> int:
    boxes = [Box(i) for i in range(256)]
    instructions = input[0].split(",")
    for inst in instructions:
        if "=" in inst:
            parts = inst.split("=")
            length = int(parts[1])
            label = parts[0]
            box_idx = hash(label)
            boxes[box_idx].insert(label, length)
        else:
            label=inst[:-1]
            box_idx = hash(label)
            boxes[box_idx].remove(label)

    score = sum([box.get_box_power() for box in boxes])
    return score

def main():
    with open("in15.txt", "r") as f:
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
        