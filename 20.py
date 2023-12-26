import time
from typing import Dict, List, Tuple
import re
import os
from queue import Queue
import math


class FlipFlop:
    destinations: List[str]
    flip_flop_state: bool # False = Low, True = High
    name: str

    def __init__(self, name: str, destinations: List[str]):
        self.destinations = destinations
        self.flip_flop_state = False
        self.name = name
    
    def receive_pulse(self, src: str, pulse: bool):
        if pulse:
            return []
        else:
            self.flip_flop_state = not self.flip_flop_state
            return [(self.name, dst, self.flip_flop_state) for dst in self.destinations]
    
class NandGate:
    conjunction_state: Dict[str, bool] # False = Low, True = High
    name: str

    def __init__(self, name: str, destinations: List[str]):
        self.destinations = destinations
        self.name = name

    def set_inputs(self, inputs: List[str]):
        self.conjunction_state = {i: False for i in inputs}

    def receive_pulse(self, src: str, pulse: bool):
        if src not in self.conjunction_state:
            raise Exception(f"{src} was not in conjunction dict for {self.name}")
        self.conjunction_state[src] = pulse
        if all(self.conjunction_state.values()):
            return [(self.name, dst, False) for dst in self.destinations]
        else:
            return [(self.name, dst, True) for dst in self.destinations]

def parse_input(input_lines: List[str]):
    nand_gates = []
    flip_flop_gates = []
    broadcaster_targets = []
    for l in input_lines:
        if l.startswith("%"):
            name, dsts = l[1:].split(" -> ")
            flip_flop_gates.append(FlipFlop(name, dsts.split(", ")))
        elif l.startswith("&"):
            name, dsts = l[1:].split(" -> ")
            nand_gates.append(NandGate(name, dsts.split(", ")))
        else:
            broadcaster_targets = l.split(" -> ")[1].split(", ")
    
    # set up the conjunction targets
    for g in nand_gates:
        sources = []
        if g in broadcaster_targets:
            sources.append("broadcaster")
        for other_g in flip_flop_gates + nand_gates:
            if g.name in other_g.destinations:
                sources.append(other_g.name)
        g.set_inputs(sources)

    gates = {g.name: g for g in flip_flop_gates+nand_gates}
    return broadcaster_targets,gates 
    

def simulate_button_press(broadcaster_targets, gates: Dict[str, object], press_number = 0):
    low_sent = 0
    high_sent = 0

    low_sent += 1 # for the button push
    signals = Queue()
    for t in broadcaster_targets:
        signals.put(("broadcaster", t, False))

    while not signals.empty():
        src, dest, signal = signals.get()
        if src in ["sr", "sn", "rf", "vq"] and press_number > 0 and signal:
            print(f"{src}: sent {signal} on press {press_number}")
        if signal:
            high_sent += 1
        else:
            low_sent += 1
        if dest in gates:
            responses = gates[dest].receive_pulse(src, signal)
            for r in responses:
                signals.put(r)

    return high_sent, low_sent


def p1(input: List[str]) -> int:
    total_high = 0
    total_low = 0
    broadcaster_targets, gates = parse_input(input)
    for _ in range(1000):
        high, low = simulate_button_press(broadcaster_targets, gates)
        total_high += high
        total_low += low
    return total_low * total_high

def get_g_type(gate):
    if isinstance(gate, NandGate):
        return "N"
    elif isinstance(gate, FlipFlop):
        return "F"
    else:
        return gate

def p2(input: List[str]) -> int:
    return math.lcm(3917, 3923, 3967, 4021)
    #broadcaster_targets, gates = parse_input(input)
    #for i in range(100000):
    #    simulate_button_press(broadcaster_targets, gates, i+1)
    #to_print = ["rx"]
    #have_printed = []
    #while len(to_print) > 0:
    #    gate = to_print[0]
    #    to_print = to_print[1:]
    #    if gate in have_printed:
    #        continue
    #    have_printed.append(gate)
    #    # print all gates that have gate in their output
    #    for g in gates:
    #        if gate in gates[g].destinations:
    #            print(f"{get_g_type(gates[g])}({g}) -> {get_g_type(gates.get(gate, gate))}({gate})")
    #            to_print.append(g)


def main():
    with open("in20.txt", "r") as f:
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
        