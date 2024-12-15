import os
import sys
import time
from enum import IntEnum
from typing import List, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 1463512
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 356166839889
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

    # TODO: Clean-up both

    ri = -1
    rj = -1
    walls: Set[PointT] = set()
    boxes: Set[PointT] = set()
    movements: List[Direction] = []
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

        it = iter(lines)
        for r, line in enumerate(it):
            if line == '\n':
                break

            line = line.strip()
            for c, char in enumerate(line):
                if char == '@':
                    ri = r
                    rj = c
                elif char == 'O':
                    boxes.add((r, c))
                elif char == '#':
                    walls.add((r, c))

        for line in it:
            line = line.strip()
            movements.extend(map(lambda chr: MAPPING[chr], line))

    for movement in movements:
        vi, vj = V[movement]

        ri_n = ri + vi
        rj_n = rj + vj
        p_n = (ri_n, rj_n)

        if p_n in boxes:
            bi = ri_n + vi
            bj = rj_n + vj
            while (bi, bj) in boxes:
                bi += vi
                bj += vj

            if (bi, bj) in walls:
                pass
            else:
                ri, rj = ri_n, rj_n
                boxes.add((bi, bj))
                boxes.remove((ri, rj_n))
        elif p_n in walls:
            pass
        else:
            ri, rj = ri_n, rj_n

    gps_sum = sum(100*r + c for r, c in boxes)

    tf = time.perf_counter()

    success = gps_sum == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {gps_sum} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
