import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

BIGBOY = True

if not BIGBOY:
    SOLUTION = 1431316
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 1051734590
    # SOLUTION = 653966888 (PART 2)
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass(slots=True)
class Garden:
    plant: str
    neighbors: int = 0
    accounted: bool = False


PointT = Tuple[int, int]


def main() -> int:
    t = time.perf_counter()

    gardens: Dict[PointT, Garden] = {}
    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            for c, plant in enumerate(line.strip()):
                gardens[r, c] = Garden(plant)

    rows = r + 1
    cols = c + 1
    V = [
        (-1, 0),    # Up
        (0, 1),     # Right
        (1, 0),     # Down
        (0, -1),    # Left
    ]

    price = 0
    for r in range(rows):
        for c in range(cols):
            garden = gardens[r, c]
            if garden.accounted:
                continue

            region = _account(r, c, garden.plant, gardens, V)
            price += len(region) * sum((4 - g.neighbors for g in region))

    tf = time.perf_counter()

    success = price == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {price} ({success})')

    return 0 if success else 1


def _account(
        r0: int,
        c0: int,
        plant: str,
        gardens: Dict[PointT, Garden],
        V: List[PointT]
) -> List[Garden]:
    arg_garden = gardens[r0, c0]

    region = [arg_garden]
    arg_garden.accounted = True

    for (vr, vc) in V:
        r = r0 + vr
        c = c0 + vc
        if (r, c) not in gardens:
            continue

        garden = gardens[r, c]
        if garden.plant != plant:
            continue

        garden.neighbors += 1
        if not garden.accounted:
            region.extend(_account(r, c, plant, gardens, V))

    return region


if __name__ == '__main__':
    exit(main())
