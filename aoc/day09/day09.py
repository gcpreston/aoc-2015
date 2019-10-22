import re
import math

from typing import Dict, Tuple, Set, List
from itertools import permutations


def main(input_file: str):
    p = re.compile(r'([a-zA-Z]+) to ([a-zA-Z]+) = (\d+)')

    routes = dict()
    locations = set()

    with open(input_file) as file:
        for line in file.readlines():
            m = p.match(line)

            loc1 = m.group(1)
            loc2 = m.group(2)
            distance = int(m.group(3))

            locations.add(loc1)
            locations.add(loc2)
            routes[(min(loc1, loc2), max(loc1, loc2),)] = distance

    print('Part 1:', part1(routes, locations))
    print('Part 2:', part2(routes, locations))


def part1(routes: Dict[Tuple[str, str], int], locations: Set[str]) -> int:
    """
    Check every permuation to see which is the shortest.
    """
    min_dist = math.inf
    for p in permutations(locations):
        complete = True
        dist = 0

        for conn in connections(p):
            if d := routes.get(conn):
                dist += d
            else:
                complete = False
                break

        if complete and dist < min_dist:
            min_dist = dist

    return min_dist


def part2(routes: Dict[Tuple[str, str], int], locations: Set[str]) -> int:
    """
    Check every permuation to check which is the longest.
    """
    max_dist = 0
    for p in permutations(locations):
        complete = True
        dist = 0

        for conn in connections(p):
            if d := routes.get(conn):
                dist += d
            else:
                complete = False
                break

        if complete and dist > max_dist:
            max_dist = dist

    return max_dist

def connections(items: Tuple) -> List:
    """
    (a1, a2, a3, ..., an) -> [(a1, a2), (a2, a3), ..., (an-1, an)]
    """
    if not items:
        return []

    ret = []
    prev = items[0]
    for cur in items[1:]:
        ret.append((min(prev, cur), max(prev, cur),))
        prev = cur

    return ret


if __name__ == '__main__':
    main('input.txt')
