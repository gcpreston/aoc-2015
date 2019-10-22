import re

from typing import Dict, Tuple


def main(input_file: str):
    p = re.compile(r'([a-zA-Z]+): capacity (\d+), durability (\d+), '
                   r'flavor (\d+), texture (\d+), calories (\d+)')

    ingredients: Dict[str, Tuple[int, int, int, int, int]] = dict()
    with open(input_file) as file:
        for line in file.readlines():
            m = p.match(line)
            ingredients[m.group(1)] = (int(m.group(2)), int(m.group(3)),
                                       int(m.group(4)), int(m.group(5)),
                                       int(m.group(6)))

    print('Part 1:', highest_score(ingredients, 100))


def highest_score(ingredients: Dict[str, Tuple[int, int, int, int, int]],
                  ts: int) -> int:
    """
    Calculate the score of the highest-scoring cookie that can be made with
    ``ts`` teaspoons of ingredients.
    """


if __name__ == '__main__':
    main('input.txt')
