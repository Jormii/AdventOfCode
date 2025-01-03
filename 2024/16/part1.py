import os
import sys
import time
import heapq
from dataclasses import dataclass
from typing import Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 83432
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass(slots=True, frozen=True)
class HeapItem:
    r: int
    c: int
    dir: int
    cost: int

    def __lt__(self, other: 'HeapItem') -> bool:
        return self.cost < other.cost


PointT = Tuple[int, int]

V = [
    (-1, 0),    # Up
    (0, 1),     # Right
    (1, 0),     # Down
    (0, -1),    # Left
]


def main() -> int:
    t = time.perf_counter()

    rr = rc = -1
    er = ec = -1
    paths: Set[PointT] = set()
    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            for c, char in enumerate(line.strip()):
                if char == 'S':
                    rr = r
                    rc = c
                    paths.add((r, c))
                elif char == 'E':
                    er = r
                    ec = c
                    paths.add((r, c))
                elif char == '.':
                    paths.add((r, c))

    dir = 1
    visited: Set[PointT] = set()
    heap = [HeapItem(rr, rc, dir, cost=0)]
    while len(heap) != 0:
        item = heapq.heappop(heap)

        r = item.r
        c = item.c
        dir = item.dir
        cost = item.cost

        if (r, c) in visited:
            continue
        visited.add((r, c))

        if r == er and c == ec:
            break

        ldir = dir - 1
        if ldir < 0:
            ldir = 3

        rdir = dir + 1
        if rdir >= len(V):
            rdir = 0

        for dir_ in (dir, ldir, rdir):
            vr, vc = V[dir_]
            r_ = r + vr
            c_ = c + vc

            if (r_, c_) in paths:
                cost_ = cost+1 + (0 if dir_ == dir else 1000)
                heapq.heappush(heap, HeapItem(r_, c_, dir_, cost_))

    tf = time.perf_counter()

    success = cost == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {cost} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
