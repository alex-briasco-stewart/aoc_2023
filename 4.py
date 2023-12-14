from typing import Dict, List, Tuple
import re


class Card:
    num: int
    winning_nums: List[int]
    our_nums: List[int]
    score: int


    def __init__(self, inp_str: str):
        m = re.match(r"Card\s+(\d+): ([\d\s]+)\|([\d\s]+)$", inp_str)
        if (m is not None):
            self.num = int(m.group(1))
            self.winning_nums = [int(x) for x in m.group(2).strip().split(' ') if len(x) > 0]
            self.our_nums = [int(x) for x in m.group(3).strip().split(' ') if len(x) > 0]

        if m is None:
            print(inp_str)
        self.score = self.get_score()

    def get_score(self) -> int:
        n_nums = sum([1 if n in self.winning_nums else 0 for n in self.our_nums ])
        return int(2**(n_nums-1))

    def get_n_matching(self) -> int:
        n_nums = sum([1 if n in self.winning_nums else 0 for n in self.our_nums ])
        return n_nums




def p1(input: List[str]) -> int:
    total_score = 0
    for c in input:
        total_score += Card(c).get_score()

    return total_score

#def p2_process_cards(cards: List[Card]):
#    total_scores = [-1 for c in cards]
#    n_cards = len(total_scores)
#    for ii in range(n_cards):
#        idx = len(cards)-ii-1
#        copies = [total_scores[j_idx] for j_idx in range(idx+1, idx+cards[idx].score+1, 1) if j_idx < n_cards]
#        print(f"matches i={ii}: {copies}")
#        if -1 in copies:
#            raise Exception("oops")
#        total_scores[idx] = len(copies) + sum(copies)
#    print(total_scores)
#    return sum(total_scores)

def p2_process_cards_att2(cards: List[Card]):
    multipliers = [1 for c in cards]
    n_cards = len(cards)
    for i in range(n_cards):
        c = cards[i]
        score = c.get_n_matching()
        for idx in range(i+1, i+score+1, 1):
            if idx < n_cards:
                multipliers[idx] += multipliers[i]
    return sum(multipliers)

def p2(input: List[str]) -> int:
    cards = []
    for c in input:
        cards.append(Card(c))
    return p2_process_cards_att2(cards)

def main():
    with open("in4.txt", "r") as f:
        lines = [l.strip('\n') for l in f.readlines()]
        print(f"part 1: {p1(lines)}")
        print(f"part 2: {p2(lines)}")

if __name__ == "__main__":
    main()