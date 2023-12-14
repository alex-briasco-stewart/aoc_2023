import time
from typing import Dict, List, Tuple
import re
import os

class HandType:
    HIGH = 1
    PAIR1 = 2
    PAIR2 = 3
    THREE = 4
    FULLHOUSE = 6
    FOUR = 7
    FIVE = 8

def get_letter_score(a, part):
    scores_1 = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    scores_2 = {
        'J': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    if part == 1:
        return scores_1[a]
    else:
        return scores_2[a]


class Hand:
    score: int
    hand_type: int
    hand_str: str
    part: int
    
    def __init__(self, hand, score, part = 1):
        letters = {}
        self.part = part
        self.score = score
        self.hand_str = hand
        for c in hand:
            if c in letters:
                letters[c] += 1
            else:
                letters[c] = 1
        val = max(letters.values())
        if val == 5:
            self.hand_type = HandType.FIVE
        elif val == 4:
            self.hand_type = HandType.FOUR
        elif val == 3:
            if min(letters.values()) == 2:
                self.hand_type = HandType.FULLHOUSE
            else:
                self.hand_type = HandType.THREE
        elif val == 2:
            if list(sorted(letters.values())) == [1, 2, 2]:
                self.hand_type = HandType.PAIR2
            else:
                self.hand_type = HandType.PAIR1
        elif val == 1:
            self.hand_type = HandType.HIGH
        else:
            raise Exception(f"Invalid hand: {hand}")

    def __repr__(self):
        return f"{self.hand_type}: {self.hand_str} ({self.score})"

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        else:
            for i in range(len(self.hand_str)):
                c_a = self.hand_str[i]
                c_b = other.hand_str[i]
                s_a = get_letter_score(c_a, self.part)
                s_b = get_letter_score(c_b, self.part)
                if (s_a > s_b):
                    return False # this Hand wins
                elif (s_b > s_a):
                    return True # other hand wins
            # if we're here. hands are totally equal. Rank the lower score hand
            return self.score < other.score

def permute_joker_hands(h, score):
    if "J" not in h:
        return [Hand(h, score, 2)]
    else:
        hands = []
        for (i, c) in enumerate(h):
            if c != "J":
                continue
            for ch in "23456789TQKA":
                hands += permute_joker_hands(h[:i] + ch + h[i+1:], score)
        return hands

def get_best_joker_hand_type(hand, score):
    #if (hand == "JJJJJ"):
    #    return HandType.FIVE
    assert('J' in hand)
    hands = permute_joker_hands(hand, score)
    hands.sort()
    return hands[-1].hand_type


def p1(input: List[str]) -> int:
    hands = []
    for l in input:
        parts = l.split(' ')
        hands.append(Hand(parts[0], int(parts[1])))
    hands.sort()
    total_score = 0
    for (i, h) in enumerate(hands):
        total_score += h.score * (i+1)
        
    return total_score

def p2(input: List[str]) -> int:
    hands = []
    for l in input:
        parts = l.split(' ')
        h = Hand(parts[0], int(parts[1]), part=2)
        if "J" in parts[0]:
            best_type = get_best_joker_hand_type(parts[0], int(parts[1]))
            h.hand_type = best_type # type: ignore
        hands.append(h)

    hands.sort()
    total_score = 0
    for (i, h) in enumerate(hands):
        print(h)
        total_score += h.score * (i+1)

    return total_score

def main():
    with open("in7.txt", "r") as f:
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
        