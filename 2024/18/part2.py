import os
import re
import sys
import time
import heapq
from typing import Set, Tuple
from dataclasses import dataclass

BIGBOY = False

if not BIGBOY:
    SOLUTION = '20,12'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = '-1'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass(slots=True, frozen=True)
class AStarNode:
    x: int
    y: int
    cost: int
    f: int
    path: Set['PointT']

    def __lt__(self, other: 'AStarNode') -> bool:
        return self.f < other.f


PointT = Tuple[int, int]

GOAL = (70, 70)
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

    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

    memory: Set[PointT] = set()
    assert (path := search_memory(memory)) is not None

    for line in lines:
        assert (search := PATTERN.search(line.strip())) is not None

        x, y = map(int, search.groups())
        memory.add((x, y))

        if (x, y) in path:
            path = search_memory(memory)
            if path is None:
                break

    solution = f'{x},{y}'

    tf = time.perf_counter()

    success = solution == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {solution} ({success})')

    return 0 if success else 1


def search_memory(memory: Set[PointT]) -> Set[PointT] | None:
    visited: Set[PointT] = set()
    heap = [AStarNode(0, 0, 0, GOAL[0]+GOAL[1], {(0, 0)})]
    while len(heap) != 0:
        node = heapq.heappop(heap)

        x = node.x
        y = node.y
        cost = node.cost
        path = node.path

        if (x, y) == GOAL:
            return path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for (vx, vy) in V:
            x_ = x + vx
            y_ = y + vy

            if 0 <= x_ < WIDTH and 0 <= y_ < HEIGHT and (x_, y_) not in memory and (x_, y_) not in visited:
                cost_ = cost + 1
                h = GOAL[0]-x_ + GOAL[1]-y_
                path_ = path.union(((x_, y_), ))

                heapq.heappush(heap, AStarNode(x_, y_, cost_, cost_ + h, path_))  # nopep8

    return None


if __name__ == '__main__':
    exit(main())
