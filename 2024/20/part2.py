import os
import sys
import time
import heapq
from typing import Dict, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 979014
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


PointT = Tuple[int, int]

CHEAT = 20
V = [
    (-1, 0),    # Up
    (0, 1),     # Right
    (1, 0),     # Down
    (0, -1),    # Left
]


def main() -> int:
    t = time.perf_counter()

    sr = sc = -1
    er = ec = -1
    paths: Set[PointT] = set()
    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            for c, char in enumerate(line.strip()):
                if char == 'S':
                    sr = r
                    sc = c
                    paths.add((r, c))
                elif char == 'E':
                    er = r
                    ec = c
                    paths.add((r, c))
                elif char == '.':
                    paths.add((r, c))

    distances = dijkstra(sr, sc, paths)

    possible = 0
    path = list(distances.keys())
    for i in range(len(path)):
        ir, ic = path[i]

        for j in range(i + 1, len(path)):
            jr, jc = path[j]

            d = abs(jr - ir) + abs(jc - ic)
            if d <= CHEAT:
                possible += (j-i - d) >= 100

    tf = time.perf_counter()

    success = possible == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {possible} ({success})')

    return 0 if success else 1


def dijkstra(sr: int, sc: int, paths: Set[PointT]) -> Dict[PointT, int]:
    heap = [(0, sr, sc)]
    distances: Dict[PointT, int] = {}
    while len(heap) != 0:
        d, r, c = heapq.heappop(heap)

        if (r, c) in distances:
            continue
        distances[r, c] = d

        for (vr, vc) in V:
            r_ = r + vr
            c_ = c + vc
            if (r_, c_) in paths:
                heapq.heappush(heap, (d + 1, r_, c_))

    return distances


if __name__ == '__main__':
    exit(main())
