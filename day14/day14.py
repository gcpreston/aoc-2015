import re

from typing import List, Dict, Set, Hashable
from dataclasses import dataclass


@dataclass
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int


def main(input_file: str, race_time: int):
    p = re.compile(r'([a-zA-Z]+) can fly (\d+) km/s for (\d+) seconds, '
                   r'but then must rest for (\d+) seconds.')

    reindeers: List[Reindeer] = []
    with open(input_file) as file:
        for line in file.readlines():
            m = p.match(line)
            reindeers.append(Reindeer(m.group(1), int(m.group(2)),
                                      int(m.group(3)), int(m.group(4))))

    print('Part 1:', winning_distance(reindeers, race_time))
    print('Part 2:', winning_points(reindeers, race_time))


def winning_distance(reindeers: List[Reindeer], seconds: int) -> int:
    """
    Calculate the distance the winning reindeer has travelled after a given
    number of seconds.
    """
    return max([distance(r, seconds) for r in reindeers])


def distance(r: Reindeer, s: int) -> int:
    """
    Calculate the distance reindeer ``r`` can travel in ``s`` seconds.
    """
    t = 0
    dist = 0

    while t < s:
        dist += r.speed * r.duration
        t += r.duration + r.rest

    return dist


def winning_points(reindeers: List[Reindeer], seconds: int) -> int:
    """
    Calculate the number of points the winning reindeer has after a given number
    of seconds.
    """
    distances: Dict[str, int] = {r.name: 0 for r in reindeers}
    counters: Dict[str, int] = {r.name: 0 for r in reindeers}
    points: Dict[str, int] = {r.name: 0 for r in reindeers}

    for t in range(seconds + 1):
        for r in reindeers:
            if counters[r.name] < r.duration:
                distances[r.name] += r.speed
            counters[r.name] = (counters[r.name] + 1) % (r.duration + r.rest)

        # give point to the reindeer in the lead
        for name in multimax(distances):
            points[name] += 1

    return max(points.values())


def multimax(d: Dict) -> Set:
    """
    Get the keys of the max value in ``d``. If the max value is unique, a set
    with a single element is returned.
    """
    maxes = set()
    biggest = 0

    for k, v in d.items():
        if v > biggest:
            biggest = v
            maxes.clear()
            maxes.add(k)
        elif v == biggest:
            maxes.add(k)

    return maxes


if __name__ == '__main__':
    main('input.txt', 2503)
