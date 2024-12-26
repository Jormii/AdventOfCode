import os
import sys
import time
import heapq
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 467
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
    path: List['PointT']

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
    costs: Dict[PointT, Tuple[int, int]] = {}
    joints: Dict[PointT, List[List[PointT]]] = {}
    heap = [HeapItem(rr, rc, dir, cost=0, path=[(rr, rc)])]
    while len(heap) != 0:
        item = heapq.heappop(heap)

        r = item.r
        c = item.c
        dir = item.dir
        cost = item.cost
        path = item.path

        if (r, c) in costs:
            add_joint = False
            dir_, cost_ = costs[r, c]
            if max(dir, dir_) - min(dir, dir_) == 2:
                add_joint = cost - cost_ <= 2  # Straight
            else:
                add_joint = cost - cost_ == 1000  # L-Turn

            if add_joint:
                if (r, c) not in joints:
                    joints[r, c] = [path]
                else:
                    joints[r, c].append(path)

            continue

        costs[r, c] = (dir, cost)

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
                path_ = path + [(r_, c_)]

                heapq.heappush(heap, HeapItem(r_, c_, dir_, cost_, path_))

    best_path = set(path)

    added_any = True
    joints_keys = list(joints.keys())
    while added_any and len(joints_keys) != 0:
        added_any = False

        for i in reversed(range(len(joints_keys))):
            r, c = joints_keys[i]
            if (r, c) not in best_path:
                continue

            for path in joints[r, c]:
                best_path.update(path)

            added_any = True
            del joints_keys[i]

    tf = time.perf_counter()

    success = len(best_path) == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {len(best_path)} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
