import os
import sys
import time
from typing import List, Tuple
from dataclasses import dataclass

BIGBOY = True

if not BIGBOY:
    SOLUTION = 1326
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 624588
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass(slots=True, repr=False, eq=False)
class Cell:
    height: int
    trailheads: int = -1


PointT = Tuple[int, int]

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
        for (vr, vc) in V:
            r = r0 + vr
            c = c0 + vc
            if 0 <= r < rows and 0 <= c < cols and topography[r][c].height == ONE:
                hike_trailheads = _hike(r, c, TWO, rows, cols, topography, V)
                trailheads_scores_sum += hike_trailheads

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
) -> int:
    # NOTE: (Not reflected, but)
    # - Apparently it's faster to call the function an additional time
    #       than introducing the {if height==NINE} branch below
    #
    # - Apparently it's faster to do the following than an if/else
    #           {if cond: return}
    #           {if other_cond: return}

    cell = topography[rh][ch]
    if cell.trailheads != -1:
        return cell.trailheads

    cell.trailheads = 0

    for (vr, vc) in V:
        r = rh + vr
        c = ch + vc
        if 0 <= r < rows and 0 <= c < cols and topography[r][c].height == height:
            if height == NINE:
                cell.trailheads += 1
            else:
                hike_trailheads = _hike(
                    r, c, height + 1, rows, cols, topography, V)
                cell.trailheads += hike_trailheads

    return cell.trailheads

if __name__ == '__main__':
    exit(main())
