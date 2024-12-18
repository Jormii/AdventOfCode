import os
import re
import sys
import time
import heapq
from typing import Set, Tuple
from dataclasses import dataclass

BIGBOY = False

if not BIGBOY:
    SOLUTION = 334
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass(slots=True, frozen=True)
class AStarNode:
    x: int
    y: int
    cost: int
    f: int

    def __lt__(self, other: 'AStarNode') -> bool:
        return self.f < other.f


PointT = Tuple[int, int]

GOAL = (70, 70)
KILOBYTE = 1024
V = [
    (0, -1),    # Up
    (1, 0),     # Right
    (0, 1),     # Down
    (-1, 0),    # Left
]

WIDTH = GOAL[1] + 1
HEIGHT = GOAL[0] + 1


def main() -> int:
    t = time.perf_counter()

    PATTERN = re.compile(r'^(\d+),(\d+)$')

    memory: Set[PointT] = set()
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()
        for i in range(KILOBYTE):
            assert (search := PATTERN.search(lines[i].strip())) is not None

            x, y = map(int, search.groups())
            memory.add((x, y))

    visited: Set[PointT] = set()
    heap = [AStarNode(0, 0, 0, GOAL[0]+GOAL[1])]
    while True:
        node = heapq.heappop(heap)

        x = node.x
        y = node.y
        cost = node.cost

        if (x, y) == GOAL:
            break

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for (vx, vy) in V:
            x_ = x + vx
            y_ = y + vy

            if 0 <= x_ < WIDTH and 0 <= y_ < HEIGHT and (x_, y_) not in memory and (x_, y_) not in visited:
                cost_ = cost + 1
                h = GOAL[0]-x_ + GOAL[1]-y_

                heapq.heappush(heap, AStarNode(x_, y_, cost_, cost_ + h))

    tf = time.perf_counter()

    success = cost == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {cost} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
