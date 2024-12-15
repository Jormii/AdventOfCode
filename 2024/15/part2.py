import os
import sys
import time
from enum import IntEnum
from typing import Dict, List, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 1486520
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 359696176529
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


PointT = Tuple[int, int]

V = [
    (-1, 0),    # Up
    (0, 1),     # Right
    (1, 0),     # Down
    (0, -1),    # Left
]
MAPPING = {
    '^': Direction.UP,
    '>': Direction.RIGHT,
    'v': Direction.DOWN,
    '<': Direction.LEFT,
}


def main() -> int:
    t = time.perf_counter()

    ri = -1
    rj = -1
    walls: Set[PointT] = set()
    boxes: Dict[PointT, bool] = {}
    movements: List[Direction] = []
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

        it = iter(lines)
        for r, line in enumerate(it):
            if line == '\n':
                break

            line = line.strip()
            for c, char in enumerate(line):
                c *= 2

                if char == '@':
                    ri = r
                    rj = c
                elif char == 'O':
                    boxes[r, c] = True
                    boxes[r, c + 1] = False
                elif char == '#':
                    walls.add((r, c))
                    walls.add((r, c + 1))

        for line in it:
            line = line.strip()
            movements.extend(map(lambda chr: MAPPING[chr], line))

    for movement in movements:
        vi, vj = V[movement]

        ri_n = ri + vi
        rj_n = rj + vj
        p_n = (ri_n, rj_n)

        if p_n in boxes:
            points = _chain_reaction(ri_n, rj_n, vi, vj, walls, boxes)
            if len(points) == 0:
                pass
            else:
                ri, rj = ri_n, rj_n

                for pi, pj in points:
                    del boxes[pi, pj]
                    del boxes[pi, pj+1]
                for pi, pj in points:
                    boxes[pi + vi, pj + vj] = True
                    boxes[pi + vi, pj+1 + vj] = False
        elif p_n in walls:
            pass
        else:
            ri, rj = ri_n, rj_n

    gps_sum = sum(100*r + c for (r, c), h in boxes.items() if h)

    tf = time.perf_counter()

    success = gps_sum == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {gps_sum} ({success})')

    return 0 if success else 1


def _chain_reaction(
        r: int,
        c: int,
        vr: int,
        vc: int,
        walls: Set[PointT],
        boxes: Dict[PointT, bool]
) -> Set[PointT]:
    is_head = boxes[r, c]
    if not is_head:
        c -= 1

    if vr != 0:
        return _chain_reaction_ver(r, c, vr, walls, boxes)
    else:
        return _chain_reaction_hor(r, c, vc, walls, boxes)


def _chain_reaction_ver(
        r: int,
        c: int,
        vr: int,
        walls: Set[PointT],
        boxes: Dict[PointT, bool]
) -> Set[PointT]:
    c2 = c + 1
    r_n = r + vr

    if (r_n, c) in walls or (r_n, c2) in walls:
        return set()

    points = {(r, c)}

    if (r_n, c) in boxes:
        is_head = boxes[r_n, c]
        if is_head:
            p = _chain_reaction_ver(r_n, c, vr, walls, boxes)
        else:
            p = _chain_reaction_ver(r_n, c - 1, vr, walls, boxes)

        if len(p) == 0:
            return set()
        else:
            points.update(p)

    if (r_n, c2) in boxes and boxes[r_n, c2]:
        p = _chain_reaction_ver(r_n, c2, vr, walls, boxes)
        if len(p) == 0:
            return set()
        else:
            points.update(p)

    return points


def _chain_reaction_hor(
        r: int,
        c: int,
        vc: int,
        walls: Set[PointT],
        boxes: Dict[PointT, bool]
) -> Set[PointT]:
    if vc == -1:
        c_n = c - 1
    else:
        c_n = c + 2

    if (r, c_n) in walls:
        return set()

    points = {(r, c)}
    if (r, c_n) in boxes:
        is_head = boxes[r, c_n]
        if not is_head:
            c_n -= 1

        p = _chain_reaction_hor(r, c_n, vc, walls, boxes)
        if len(p) == 0:
            return set()
        else:
            points.update(p)

    return points


if __name__ == '__main__':
    exit(main())
