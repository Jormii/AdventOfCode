import os
import sys
import time
from typing import List
from bisect import bisect

BIGBOY = False

if not BIGBOY:
    SOLUTION = 4903
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

DIRECTIONS = [
    (-1, 0),    # Up
    (0, 1),     # Right
    (1, 0),     # Down
    (0, -1),    # Left
]


def main() -> int:
    t = time.perf_counter()

    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

    guard_row = -1
    guard_col = -1

    rows = len(lines)
    cols = len(lines[0]) - 1
    in_row: List[List[int]] = [[] for _ in range(rows)]
    in_column: List[List[int]] = [[] for _ in range(cols)]

    for r, line in enumerate(lines):
        for c, char in enumerate(line.strip()):
            if char == '^':
                guard_row = r
                guard_col = c
            elif char == '#':
                in_row[r].append(c)
                in_column[c].append(r)

    inside_map = True
    direction_idx = 0  # Up
    visited = {(guard_row, guard_col)}
    while inside_map:
        if direction_idx == 0:
            # Up
            arr = in_column[guard_col]
            idx = bisect(arr, guard_row)

            if idx == 0:
                inside_map = False
                steps = guard_row + 1
            else:
                steps = guard_row - arr[idx - 1]
        elif direction_idx == 1:
            # Right
            arr = in_row[guard_row]
            idx = bisect(arr, guard_col)

            if idx == len(arr):
                inside_map = False
                steps = rows - guard_col
            else:
                steps = arr[idx] - guard_col
        elif direction_idx == 2:
            # Down
            arr = in_column[guard_col]
            idx = bisect(arr, guard_row)

            if idx == len(arr):
                inside_map = False
                steps = cols - guard_row
            else:
                steps = arr[idx] - guard_row
        elif direction_idx == 3:
            # Left
            arr = in_row[guard_row]
            idx = bisect(arr, guard_col)

            if idx == 0:
                inside_map = False
                steps = guard_col + 1
            else:
                steps = guard_col - arr[idx - 1]

        vr, vc = DIRECTIONS[direction_idx]
        for _ in range(steps - 1):  # -1 to not step into an obstacle
            guard_row += vr
            guard_col += vc
            visited.add((guard_row, guard_col))

        if direction_idx != 3:
            direction_idx += 1  # Up -> Right -> Down -> Left
        else:
            direction_idx = 0   # Left -> Up

    visited_count = len(visited)

    tf = time.perf_counter()

    success = visited_count == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {visited_count} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
