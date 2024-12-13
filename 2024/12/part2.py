import os
import sys
import time
from collections import deque
from typing import Dict, List, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 821428
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 653966888
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
    LEN_V = len(V)

    price = 0
    for plant, points in gardens.items():
        while len(points) != 0:
            r, c = points.pop()
            queue = deque([(r, c)])
            region: Dict[PointT, List[int]] = {}
            while len(queue) != 0:
                r0, c0 = queue.pop()
                neighbors: List[int] = []

                for i, (vr, vc) in enumerate(V):
                    r = r0 + vr
                    c = c0 + vc
                    if (r, c) in points:
                        neighbors.append(i)
                        region[(r, c)] = []

                        queue.append((r, c))
                        points.remove((r, c))
                    elif (r, c) in region:
                        neighbors.append(i)

                region[r0, c0] = neighbors

            corners = 0
            for (r, c), neighbors in region.items():
                n = len(neighbors)

                if n == 0:
                    corners += 4
                elif n == 1:
                    corners += 2
                elif n == 2:
                    i = min(neighbors)
                    j = max(neighbors)

                    # Corners in binary: 0b0011, 0b0110, 0b1100, 0b1001

                    if (j - i) == 1 or (i == 0 and j == 3):
                        corners += 1 + not_present(r, c, region, i, j, V)
                elif n == 3:
                    for i in range(LEN_V):
                        if i in neighbors:
                            continue  # Missing {i} is {V[i]} opposite to "T"

                        i += 2
                        if i >= LEN_V:
                            i -= LEN_V

                        j = i - 1
                        corners += not_present(r, c, region, i, j, V)

                        j = i + 1
                        if j == LEN_V:
                            j = 0

                        corners += not_present(r, c, region, i, j, V)

                        break
                elif n == 4:
                    for i in neighbors:
                        j = i + 1
                        if j == LEN_V:
                            j = 0

                        corners += not_present(r, c, region, i, j, V)

            price += len(region) * corners

    tf = time.perf_counter()

    success = price == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {price} ({success})')

    return 0 if success else 1


def not_present(
        r: int,
        c: int,
        region: Dict[PointT, List[int]],
        i: int,
        j: int,
        V: List[PointT]
) -> bool:
    vr_i, vc_i = V[i]
    vr_j, vc_j = V[j]
    diagonal = (r + vr_i + vr_j, c + vc_i + vc_j)

    return diagonal not in region


if __name__ == '__main__':
    exit(main())
