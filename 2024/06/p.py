import os
import sys
import time
from typing import Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 4903
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

PointT = Tuple[int, int]

DIRECTIONS = [
    (-1, 0),    # Up
    (0, 1),     # Right
    (1, 0),     # Down
    (0, -1),    # Left
]


def main() -> int:
    t = time.perf_counter()

    guard_row = 0
    guard_col = 0
    obstacles: Set[PointT] = set()

    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            for c, char in enumerate(line):
                match char:
                    case '#':
                        obstacles.add((r, c))
                    case '^':
                        guard_row = r
                        guard_col = c

    rows = r + 1    # r= Index of last row
    cols = c        # c= Index of \n

    visited: Set[PointT] = set()

    direction_idx = 0
    dr, dc = DIRECTIONS[direction_idx]
    while 0 <= guard_row < rows and 0 <= guard_col < cols:
        visited.add((guard_row, guard_col))

        next_guard_row = guard_row + dr
        next_guard_col = guard_col + dc
        while ((next_guard_row, next_guard_col)) in obstacles:
            direction_idx += 1
            if direction_idx == len(DIRECTIONS):
                direction_idx = 0

            dr, dc = DIRECTIONS[direction_idx]

            next_guard_row = guard_row + dr
            next_guard_col = guard_col + dc

        guard_row = next_guard_row
        guard_col = next_guard_col

    visited_count = len(visited)

    tf = time.perf_counter()

    success = visited_count == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {visited_count} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
