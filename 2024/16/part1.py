import os
import sys
import time
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

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

    @staticmethod
    def new(r: int, c: int, dir: int, cost: int) -> 'HeapItem':
        return HeapItem(r, c, dir, cost)


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

    nodes: Dict[PointT, List[int]] = {}
    for (r, c) in paths:
        dirs: List[int] = []
        for dir, (vr, vc) in enumerate(V):
            if (r + vr, c + vc) in paths:
                dirs.append(dir)

        if len(dirs) == 2:
            dir = min(dirs)
            other_dir = max(dirs)
            if (dir == 0 and other_dir == 2) or (dir == 1 and other_dir == 3):
                continue

        nodes[r, c] = dirs

    graph: Dict[Tuple[int, PointT], Tuple[int, PointT]] = {}
    for (r, c), dirs in nodes.items():
        for dir in dirs:
            if (dir, (r, c)) in graph:
                continue

            vr, vc = V[dir]

            r_ = r + vr
            c_ = c + vc
            distance = 1
            while (r_, c_) not in nodes:
                r_ += vr
                c_ += vc
                distance += 1

            graph[dir, (r, c)] = (distance, (r_, c_))
            graph[(dir + 2) % 4, (r_, c_)] = (distance, (r, c))

    dir = 1
    visited: Set[PointT] = set()
    heap = [HeapItem.new(rr, rc, dir, cost=0)]
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

        if (dir, (r, c)) in graph:
            distance, (r_, c_) = graph[dir, (r, c)]
            heapq.heappush(
                heap,
                HeapItem.new(r_, c_, dir, cost + distance)
            )

        if (ldir, (r, c)) in graph:
            distance, (r_, c_) = graph[ldir, (r, c)]
            heapq.heappush(
                heap,
                HeapItem.new(r_, c_, ldir, cost+1000 + distance)
            )

        if (rdir, (r, c)) in graph:
            distance, (r_, c_) = graph[rdir, (r, c)]
            heapq.heappush(
                heap,
                HeapItem.new(r_, c_, rdir, cost+1000 + distance)
            )

    tf = time.perf_counter()

    success = cost == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {cost} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
