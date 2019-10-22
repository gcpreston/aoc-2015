import re

from typing import Dict, Tuple
from collections import defaultdict
from itertools import permutations


def main(input_file: str):
    p = re.compile(r'([a-zA-Z]+) would (gain|lose) (\d+) '
                   r'happiness units by sitting next to ([a-zA-Z]+)')

    deltas: Dict[str, Dict[str, int]] = defaultdict(dict)

    with open(input_file) as file:
        for line in file.readlines():
            m = p.match(line)

            person1 = m.group(1)
            person2 = m.group(4)
            amount = int(m.group(3))
            if m.group(2) == 'lose':
                amount *= -1

            deltas[person1][person2] = amount

    print('Part 1:', optimal_arrangement(deltas))

    for person in list(deltas.keys()):
        deltas[person]['you'] = 0
        deltas['you'][person] = 0

    print('Part 2:', optimal_arrangement(deltas))


def optimal_arrangement(deltas: Dict[str, Dict[str, int]]) -> int:
    """
    Finds the total change in happiness for the optimal seating arrangement.
    """
    max_change = 0

    # could be slightly optimized with a permutation function which did not
    # generate cyclic rotations
    for p in permutations(deltas.keys()):
        if (change := calc_change(p, deltas)) > max_change:
            max_change = change

    return max_change


def calc_change(arrangement: Tuple[str],
                deltas: Dict[str, Dict[str, int]]) -> int:
    """
    Calculates the total change in happiness for a given seating arrangement.
    """
    change = 0
    size = len(arrangement)

    for i in range(size):
        change += deltas[arrangement[i]][arrangement[(i - 1) % size]]
        change += deltas[arrangement[i]][arrangement[(i + 1) % size]]

    return change


if __name__ == '__main__':
    main('input.txt')
