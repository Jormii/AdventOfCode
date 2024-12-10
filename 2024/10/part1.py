import os
import sys
import time
from typing import Dict, List, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 709
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

PointT = Tuple[int, int]


def main() -> int:
    t = time.perf_counter()

    zeros: List[PointT] = []
    topography: List[List[int]] = []
    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            row = list(map(int, line.strip()))

            for c, height in enumerate(row):
                if height == 0:
                    zeros.append((r, c))
            topography.append(row)

    rows = r + 1
    cols = c + 1
    trailheads_scores_sum = 0

    V = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]
    cache: Dict[PointT, Set[PointT]] = {}
    for (r0, c0) in zeros:
        trailheads: Set[PointT] = set()
        for (vr, vc) in V:
            r = r0 + vr
            c = c0 + vc
            if 0 <= r < rows and 0 <= c < cols and topography[r][c] == 1:
                hike_trailheads = _hike(
                    r, c, 2,
                    rows, cols, topography, V, cache
                )

                trailheads.update(hike_trailheads)

        trailheads_scores_sum += len(trailheads)

    tf = time.perf_counter()

    success = trailheads_scores_sum == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {trailheads_scores_sum} ({success})')

    return 0 if success else 1


def _hike(
        rh: int,
        ch: int,
        height: int,
        rows: int,
        cols: int,
        topography: List[List[int]],
        V: List[PointT],
        cache: Dict[PointT, Set[PointT]],
) -> Set[PointT]:
    if (rh, ch) in cache:
        return cache[rh, ch]

    trailheads: Set[PointT] = set()
    for (vr, vc) in V:
        r = rh + vr
        c = ch + vc
        if 0 <= r < rows and 0 <= c < cols and topography[r][c] == height:
            if height == 9:
                trailheads.add((r, c))
            else:
                hike_trailheads = _hike(
                    r, c, height + 1,
                    rows, cols, topography, V, cache
                )

                trailheads.update(hike_trailheads)

    cache[rh, ch] = trailheads

    return trailheads


if __name__ == '__main__':
    exit(main())
