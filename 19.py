import time
from typing import Dict, List, Tuple, Callable, Optional
import re
import os
from queue import Queue

class Rule:
    rule_fn: Callable

    def __init__(self, rule_str: str):
        if ":" not in rule_str:
            self.rule_fn = lambda _: rule_str
            self.type = "direct"
            self.dest = rule_str
        else:
            test, dest = rule_str.split(":")
            self.dest = dest
            if ">" in test:
                opt, val = test.split(">")
                int_val = int(val)
                self.rule_fn = lambda d: dest if d[opt] > int_val else None

                self.type = "gt"
                self.opt = opt
                self.val = int_val
            else:
                opt, val = test.split("<")
                int_val = int(val)

                self.type = "lt"
                self.val = int_val
                self.opt = opt
                self.rule_fn = lambda d: dest if d[opt] < int_val else None

    def parse_range_dict(self, r_dict: dict):
        if self.type == "direct":
            # nothing to do
            return self.dest, r_dict, None
        #r_dict is of the form 
        # {
        #   x: (low, high),
        #   y: (low, high),
        #   a: (low, high),
        #   b: (low, high),
        # }
        # and we will split on one of the axes
        # return two ranges: passing, falling
        dest, pass_range, fail_range = self.parse_range(r_dict[self.opt])
        pass_dict = None
        fail_dict = None

        if pass_range is not None:
            pass_dict = r_dict.copy()
            pass_dict[self.opt] = pass_range
        if fail_range is not None:
            fail_dict = r_dict.copy()
            fail_dict[self.opt] = fail_range

        return dest, pass_dict, fail_dict
    def parse_range(self, r: Tuple[int, int]):
        if self.type == "direct":
            return self.dest, r, None
        elif self.type == "gt":
            if self.val > r[1]: # nothing passes
                return self.dest, None, r
            elif self.val < r[0]: # everything passes
                return self.dest, r, None
            else:
                return self.dest, (self.val+1, r[1]), (r[0], self.val)
        elif self.type == "lt":
            if self.val > r[1]:
                return self.dest, r, None
            elif self.val < r[0]:
                return self.dest, None, r
            else:
                return self.dest, (r[0], self.val-1), (self.val, r[1])
        else:
            raise Exception('oopsie')

class Workflow:
    name: str
    rules: List[Rule]

    def __init__(self, name, _rules):
        self.name = name
        self.rules = [Rule(r) for r in _rules]
    
    def solve_item(self, item: dict):
        for r in self.rules:
            s = r.rule_fn(item)
            if s is not None:
                return s
        raise Exception("hit the end of the rules?")
    
    def solve_range(self, r_dict: dict):
        # returns a dict of (dest, dict)
        curr_dict = r_dict

        accepted = []
        for rule in self.rules:
            dst, accept, reject = rule.parse_range_dict(curr_dict)
            if accept is not None:
                accepted.append((dst, accept))
            if reject is None:
                return accepted
            else:
                curr_dict = reject

def parse_workflow(in_line: str) -> Workflow:
    m = re.match("^([a-z]+){(.+)}$", in_line)
    if m is None:
        raise Exception(f"bad match: {m}")
    workflow_name = m.group(1)
    rules = m.group(2).split(",")
    return Workflow(workflow_name, rules)

def parse_item(in_line: str) -> dict:
    m = re.match("^{x=(-?[0-9]+),m=(-?[0-9]+),a=(-?[0-9]+),s=(-?[0-9]+)}$", in_line)
    if m is None:
        raise Exception(f"Failed to match item: {in_line}")
    return {
        "x": int(m.group(1)),
        "m": int(m.group(2)),
        "a": int(m.group(3)),
        "s": int(m.group(4)),
    }

def parse_input(input_lines: List[str]) -> Tuple[Dict[str, Workflow], List[dict]]:
    workflows = {}
    items = []
    parsing_workflows = True
    for l in input_lines:
        if l == "":
            parsing_workflows = False
        elif parsing_workflows:
            w = parse_workflow(l)
            workflows[w.name] = w
        else:
            items.append(parse_item(l))
    
    return workflows, items

def solve_item(item: dict, workflows: Dict[str, Workflow]):
    w = workflows["in"]
    while True:
        next = w.solve_item(item)
        if next == "R":
            return "R"
        elif next == "A":
            return "A"
        else:
            w = workflows[next]

def item_score(item: dict):
    return sum(item.values())

def p1(input: List[str]) -> int:
    workflows, items = parse_input(input)
    total_score = 0
    for i in items:
        #print(f"{i} => {solve_item(i, workflows)}")
        if solve_item(i, workflows) == "A":
            total_score += item_score(i)
    return total_score

def p2(input: List[str]) -> int:
    workflows, _ = parse_input(input)

    start_range = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000)
    }
    #wkflw = parse_workflow("px{a<2006:qkq,m>2090:A,rfg}")
    #for target_name, d in wkflw.solve_range(start_range):
    #    print(f"{target_name}: {d}")
    #return -1
    ranges = Queue()
    ranges.put(("in", start_range))

    total_score = 0
    while not ranges.empty():
        wkflow_name, range = ranges.get()
        names_and_ranges = workflows[wkflow_name].solve_range(range)
        for tup in names_and_ranges:
            if tup[0] == "A":
                ar = tup[1]
                combs = 1
                for k in "xmas":
                    combs *= ((ar[k][1] + 1) - ar[k][0])
                total_score += combs
            elif tup[0] != "R":
                ranges.put(tup)
            # else rejected
    return total_score

def main():
    with open("in19.txt", "r") as f:
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
        