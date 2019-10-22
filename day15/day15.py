import re

from typing import Dict, Tuple, List
from operator import mul
from functools import reduce


def main(input_file: str):
    p = re.compile(r'([a-zA-Z]+): capacity (-?\d+), durability (-?\d+), '
                   r'flavor (-?\d+), texture (-?\d+), calories (-?\d+)')

    ingredients: Dict[str, Dict[str, int]] = dict()
    with open(input_file) as file:
        for line in file.readlines():
            m = p.match(line)
            ingredients[m.group(1)] = {
                'capacity': int(m.group(2)),
                'durability': int(m.group(3)),
                'flavor': int(m.group(4)),
                'texture': int(m.group(5)),
                'calories': int(m.group(6))
            }

    print('Part 1:', highest_score(ingredients, 100))


def highest_score(ingredients: Dict[str, Dict[str, int]], ts: int) -> int:
    """
    Calculate the score of the highest-scoring cookie that can be made with
    ``ts`` teaspoons of ingredients.
    """
    # TODO: Calculate magic number
    print('Computing possible ratios...')
    possible_ratios = combination_sum(4, ts)
    print('Done.')
    biggest = 0

    print('Checking ratios...')
    for r in possible_ratios:
        named_ratio = {
            'Sprinkles': r[0],
            'PeanutButter': r[1],
            'Frosting': r[2],
            'Sugar': r[3]
        }
        score = calc_score(ingredients, named_ratio)

        if score > biggest:
            biggest = score

    return biggest


def calc_score(ingredients: Dict[str, Dict[str, int]],
               ratios: Dict[str, int]) -> int:
    """
    Calculate the total score of a cookie based on the ratios of ingredients.

    ratios: {
        'Sprinkes': 17,
        'PeanutButter': 18,
        'Frosting': 31,
        'Sugar': 34
    }

    ingredients: {
        'Sprinkles': {
            'capacity': 5,
            'durability': -1,
            'flavor': 0,
            'texture': 0,
            'calories': 5
        }
        'PeanutButter': {
            'capacity': ...
        }
        ...
    }
    """
    properties = [0, 0, 0, 0, 0]  # TODO: Calculate this from ingredients
    for ingr in ratios:
        ingr_properties = [val * ratios[ingr] for prop, val in
                           ingredients[ingr].items()]
        properties = [sum(pair) for pair in zip(properties, ingr_properties)]

    # get rid of negative values
    properties = [p if p > 0 else 0 for p in properties]
    # product of everything but calories
    return reduce(mul, properties[:-1])


def combination_sum(k: int, n: int) -> List[List[int]]:
    """
    Find all combinations of ``k`` numbers which add to ``n``. Raises
    ``ValueError`` if ``k`` or ``n`` is negative or 0.
    """
    if any([i <= 0 for i in (k, n,)]):
        raise ValueError('k and n must be positive integers')

    memory: Dict[Tuple[int, int], List[List[int]]] = dict()

    def _do_work(_k: int, _n: int) -> List[List[int]]:
        # base case
        if _k == 1:
            return [[_n]]

        # check if value was already computed
        if possible := memory.get((_k, _n,)):
            return possible

        # recursive case
        combos = []
        for i in range(1, _n):
            for combo in _do_work(_k - 1, _n - i):
                new_combo = sorted(combo + [i])
                if new_combo not in combos:
                    combos.append(new_combo)

        memory[(_k, _n)] = combos
        return combos

    return _do_work(k, n)


if __name__ == '__main__':
    main('input.txt')
