from typing import Dict, List, Tuple
import re

class Range:
    inStart: int
    outStart: int
    rangeSize: int

    def __init__(self, inStart, outStart, size):
        self.inStart = inStart
        self.outStart = outStart
        self.rangeSize = size

    def contains_input(self, inp_val):
        return inp_val >= self.inStart and inp_val < self.inStart + self.rangeSize

    def map(self, inp_val):
        assert(self.contains_input(inp_val))
        return self.outStart + inp_val - self.inStart

class ValueRange:
    # is inclusive
    start: int
    end: int
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def overlaps_with_range(self, r: Range) -> bool:
        # check all the endpoints

        # r.End < self.start
        if r.inStart + r.rangeSize - 1 < self.start:
            return False
        if r.inStart > self.end:
            return False
        
        return True

def split_value_range_on_range(vr: ValueRange, r: Range) -> Tuple[ValueRange, List[ValueRange]]:
    assert(vr.overlaps_with_range(r))

    start = max(vr.start, r.inStart)
    end = min(vr.end, r.inStart+r.rangeSize-1)

    offset = r.outStart - r.inStart
    mapped_range = ValueRange(start+offset, end+offset)
    remainders = []

    if vr.start < r.inStart: # there's part of the VR before the Range
        remainders.append(ValueRange(vr.start, r.inStart-1))

    if (vr.end > r.inStart+r.rangeSize-1):
        remainders.append(ValueRange(r.inStart+r.rangeSize, vr.end))

    # return value is the mapped_value, outside_unmapped_values
    return (mapped_range, remainders)

class Map:
    inT: str
    outT: str
    ranges: List[Range]
    
    def __init__(self, inT, outT):
        self.inT = inT
        self.outT = outT
        self.ranges = []

    def __repr__(self):
        return f"{self.inT}-to-{self.outT}: {len(self.ranges)} ranges"
    
    def add_range(self, range):
        self.ranges.append(range)

    def map_in_to_out(self, in_val: int):
        valid_ranges = list(filter(lambda r: r.contains_input(in_val), self.ranges))
        if len(valid_ranges) == 2:
            raise Exception("overlap!")
        if len(valid_ranges) == 1:
            return valid_ranges[0].map(in_val)
        else:
            return in_val

    def map_value_range(self, _vr: ValueRange) -> List[ValueRange]:
        mapped_ranges = []

        curr_ranges = [_vr]
        temp_ranges = []
        for r in self.ranges:
            for vr in curr_ranges:
                if (vr.overlaps_with_range(r)):
                    m_r, outside_ranges = split_value_range_on_range(vr, r)
                    mapped_ranges.append(m_r)
                    # temp_ranges is everything that wasnt mapped here, but might be later
                    temp_ranges += outside_ranges
                else:
                    temp_ranges.append(vr)
            curr_ranges = temp_ranges
            temp_ranges = []
        # everything remaining is mapped directly
        return mapped_ranges + curr_ranges
        

def get_map_from_string(line: str):
    m = re.match(r"^([a-z]+)-to-([a-z]+) map:$", line.strip())
    if m:
        return Map(m.group(1), m.group(2))
    raise Exception("no map")

def get_range_from_line(line: str):
    m = re.match(r"^(\d+)\s+(\d+)\s+(\d+)$", line.strip())
    if m:
        return Range(int(m.group(2)), int(m.group(1)), int(m.group(3)))
    raise Exception("no range")

def parse_input(input_lines: List[str]) -> Tuple[List[int], List[Map]]:
    seeds = [int(val) for val in input_lines[0].split("seeds: ")[1].strip().split(" ")]

    line_idx = 3
    maps = []
    curr_map = get_map_from_string(input_lines[2])
    maps.append(curr_map)
    while (line_idx < len(input_lines)):
        l = input_lines[line_idx]
        if (l == ""):
            line_idx += 1
            continue
        if "map" in l:
            curr_map = get_map_from_string(l)
            maps.append(curr_map)
        else: # range
            curr_map.add_range(get_range_from_line(l))
        line_idx += 1

    return seeds, maps

def get_location_of_seed(seed: int, maps: List[Map]) -> int:
    curr_type = "seed"
    val = seed
    while curr_type != "location":
        m = [m for m in maps if m.inT == curr_type][0]
        new_val = m.map_in_to_out(val)
        #print(f"seed {seed} {curr_type}={val} -> {m.outT}={new_val}")
        val = new_val
        curr_type = m.outT
    return val

def get_min_location_of_range(seed_start: int, seed_range_size: int, maps: List[Map]) -> int:
    start_range = ValueRange(seed_start, seed_start + seed_range_size-1)
    curr_type = "seed"
    value_ranges = [start_range]
    while curr_type != "location":
        m = [m for m in maps if m.inT == curr_type][0]
        next_vrs: List[ValueRange] = []
        for vr in value_ranges:
            next_vrs += m.map_value_range(vr)
        value_ranges = next_vrs

        curr_type = m.outT
    
    return min([vr.start for vr in value_ranges])


def p1(input: List[str]) -> int:
    seeds, maps = parse_input(input)
    scores = [get_location_of_seed(s, maps) for s in seeds]
    #for (seed, score) in zip(seeds, scores):
    #    print(f"seed {seed}: location={score}")
    return min(scores)


def p2(input: List[str]) -> int:
    seed_ranges, maps = parse_input(input)
    seed_starts = [s for (i, s) in enumerate(seed_ranges) if i % 2 == 0]
    seed_lengths = [s for (i, s) in enumerate(seed_ranges) if i % 2 == 1]

    lowest_locations = []
    for s, l in zip(seed_starts, seed_lengths):
        lowest_locations.append(get_min_location_of_range(s, l, maps))
    return min(lowest_locations)

def main():
    with open("in5.txt", "r") as f:
        lines = [l.strip('\n') for l in f.readlines()]
        print(f"part 1: {p1(lines)}")
        print(f"part 2: {p2(lines)}")

if __name__ == "__main__":
    main()