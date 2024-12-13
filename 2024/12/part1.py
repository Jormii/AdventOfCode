import os
import sys
import time
from collections import deque
from typing import Dict, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 1431316
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 1051734590
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


PointT = Tuple[int, int]


def main() -> int:
    t = time.perf_counter()

    gardens: Dict[str, Set[PointT]] = {}
    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            for c, plant in enumerate(line.strip()):
                if plant not in gardens:
                    gardens[plant] = {(r, c)}
                else:
                    gardens[plant].add((r, c))

    V = [
        (-1, 0),    # Up
        (0, 1),     # Right
        (1, 0),     # Down
        (0, -1),    # Left
    ]

    price = 0
    for plant, points in gardens.items():
        while len(points) != 0:
            r, c = points.pop()
            queue = deque([(r, c)])
            region: Dict[PointT, int] = {}
            while len(queue) != 0:
                neighbors = 0
                r0, c0 = queue.pop()

                for (vr, vc) in V:
                    r = r0 + vr
                    c = c0 + vc
                    if (r, c) in points:
                        neighbors += 1
                        region[(r, c)] = 0

                        queue.append((r, c))
                        points.remove((r, c))
                    elif (r, c) in region:
                        neighbors += 1

                region[r0, c0] = neighbors

            price += len(region) * sum((4 - n for n in region.values()))

    tf = time.perf_counter()

    success = price == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {price} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
