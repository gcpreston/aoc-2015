from enum import Enum, auto
from typing import Tuple


class Operators(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    GETS = auto()


wires = dict()


def main():
    parse_wires()

    p1 = compute_signal('a')
    print('Part 1:', p1)

    parse_wires()
    wires['b'] = p1
    print('Part 2:', compute_signal('a'))


def parse_wires(fn: str = 'input.txt'):
    with open(fn) as file:
        d: Tuple

        for line in file.readlines():
            spl = line.strip().split()
            if 'AND' in spl:
                wires[spl[4]] = (Operators.AND, [spl[0], spl[2]])
            elif 'OR' in spl:
                wires[spl[4]] = (Operators.OR, [spl[0], spl[2]])
            elif 'NOT' in spl:
                wires[spl[3]] = (Operators.NOT, [spl[1]])
            elif 'LSHIFT' in spl:
                wires[spl[4]] = (Operators.LSHIFT, [spl[0], spl[2]])
            elif 'RSHIFT' in spl:
                wires[spl[4]] = (Operators.RSHIFT, [spl[0], spl[2]])
            else:
                wires[spl[2]] = (Operators.GETS, [spl[0]])


def compute_signal(name_or_val: str):
    """
    Calculate the value for a given name on a given wire mapping.
    """
    if name_or_val.isdigit():
        return int(name_or_val)

    name = name_or_val
    wire = wires.get(name)

    if type(wire) == int:
        # wire has been evaluated
        return wire

    # wire: Tuple[Operation, List[Union[str, int]]]
    op, args = wire

    wires[name] = eval_function[op](*[compute_signal(a) for a in args])
    return wires[name]


def wrap(n):
    return (65536 + n) % 65536


eval_function = {
    Operators.AND: lambda a, b: wrap(a & b),
    Operators.OR: lambda a, b: wrap(a | b),
    Operators.NOT: lambda a: ~a,
    Operators.LSHIFT: lambda a, b: wrap(a << b),
    Operators.RSHIFT: lambda a, b: wrap(a >> b),
    Operators.GETS: lambda a: int(a)
}


if __name__ == '__main__':
    main()
