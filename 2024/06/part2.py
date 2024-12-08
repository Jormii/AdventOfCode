import os
import sys
import time
from typing import Dict, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 1911
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

    flow: Dict[PointT, int] = {}

    for obstacle in obstacles:
        for direction_idx, (dr, dc) in enumerate(DIRECTIONS):
            r, c = obstacle
            direction_idx_flow = direction_idx + 2
            if direction_idx_flow >= len(DIRECTIONS):
                direction_idx_flow -= len(DIRECTIONS)

            r += dr
            c += dc
            flag = 1 << direction_idx_flow
            while 0 <= r < rows and 0 <= c < cols:
                point = (r, c)
                if point in obstacles:
                    break
                elif point not in flow:
                    flow[point] = flag
                else:
                    flow[point] |= flag

                r += dr
                c += dc

    loops: Set[PointT] = set()
    visited: Dict[PointT, int] = {}

    direction_idx = 0
    dr, dc = DIRECTIONS[direction_idx]
    while 0 <= guard_row < rows and 0 <= guard_col < cols:
        flag = 1 << direction_idx
        point = (guard_row, guard_col)

        if point not in visited:
            visited[point] = flag
        else:
            visited[point] |= flag

        next_guard_row = guard_row + dr
        next_guard_col = guard_col + dc
        next_point = (next_guard_row, next_guard_col)
        if 0 <= next_guard_row < rows and 0 <= next_guard_col < cols \
                and point in flow \
                and next_point not in visited and next_point not in obstacles:
            direction_idx_loop = direction_idx + 1
            if direction_idx_loop == len(DIRECTIONS):
                direction_idx_loop = 0

            flag = 1 << direction_idx_loop
            if flow[point] & flag:
                obstacles.add(next_point)
                if _loops(
                    guard_row, guard_col, direction_idx_loop,
                    rows, cols, visited, obstacles
                ):
                    loops.add(next_point)
                obstacles.remove(next_point)

        if ((next_guard_row, next_guard_col)) not in obstacles:
            guard_row = next_guard_row
            guard_col = next_guard_col
        else:
            direction_idx += 1
            if direction_idx == len(DIRECTIONS):
                direction_idx = 0

            dr, dc = DIRECTIONS[direction_idx]

    tf = time.perf_counter()

    success = len(loops) == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {len(loops)} ({success})')

    return 0 if success else 1


def _loops(
        guard_row: int,
        guard_col: int,
        direction_idx: int,
        rows: int,
        cols: int,
        visited: Dict[PointT, int],
        obstacles: Set[PointT],
) -> bool:
    visited_loop = dict(visited)
    dr, dc = DIRECTIONS[direction_idx]
    while 0 <= guard_row < rows and 0 <= guard_col < cols:
        flag = 1 << direction_idx
        point = (guard_row, guard_col)

        if point not in visited_loop:
            visited_loop[point] = flag
        elif visited_loop[point] & flag:
            return True
        else:
            visited_loop[point] |= flag

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

    return False


if __name__ == '__main__':
    exit(main())
