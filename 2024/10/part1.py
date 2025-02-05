import os
import sys
import time
from typing import List, Set, Tuple
from dataclasses import dataclass, field

BIGBOY = False

if not BIGBOY:
    SOLUTION = 709
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 433087
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


PointT = Tuple[int, int]


@dataclass(slots=True)
class Cell:
    height: int
    visited: bool = False
    trailheads: Set[PointT] = field(default_factory=set)


ZERO = ord('0')
ONE = ord('1')
TWO = ord('2')
NINE = ord('9')


def main() -> int:
    t = time.perf_counter()

    zeros: List[PointT] = []
    topography: List[List[Cell]] = []
    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            row: List[Cell] = []

            for c, height in enumerate(map(ord, line.strip())):
                row.append(Cell(height))

                if height == ZERO:
                    zeros.append((r, c))

            topography.append(row)

    rows = r + 1
    cols = len(row)
    trailheads_scores_sum = 0

    V = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]
    for (r0, c0) in zeros:
        trailheads: Set[PointT] = set()
        for (vr, vc) in V:
            r = r0 + vr
            c = c0 + vc
            if 0 <= r < rows and 0 <= c < cols and topography[r][c].height == ONE:
                hike_trailheads = _hike(r, c, TWO, rows, cols, topography, V)
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
        topography: List[List[Cell]],
        V: List[PointT],
) -> Set[PointT]:
    cell = topography[rh][ch]

    if cell.visited:
        return cell.trailheads

    for (vr, vc) in V:
        r = rh + vr
        c = ch + vc
        if 0 <= r < rows and 0 <= c < cols and topography[r][c].height == height:
            if height == NINE:
                cell.trailheads.add((r, c))
            else:
                hike_trailheads = _hike(
                    r, c, height + 1, rows, cols, topography, V)
                cell.trailheads.update(hike_trailheads)

    cell.visited = True
    return cell.trailheads


if __name__ == '__main__':
    exit(main())
