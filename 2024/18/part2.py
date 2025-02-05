import os
import sys
import time
import heapq
from typing import List, Set, Tuple
from dataclasses import dataclass

BIGBOY = False

if not BIGBOY:
    SOLUTION = '20,12'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = '-1'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

# https://topaz.github.io/paste/#XQAAAQDfAQAAAAAAAAAzHIoib6pRzyfA3vvMmTvx5m4DtLDvEv8xRFiT/iYBaijO1XCmDCtq4RWMxJbduxJUye0f5QqOSQR4aMoeUjQLeaMUi8bOMrbuAEyBc2Xm/IAnk3puGiA1nW2zXC66mrKIkkz6VFp7C2rlx9c+ZTQ8FoDnYs3mE81oyT1Za/Ie8LDObuWTfA5qiXPBCJGLYxoIl8FSftzLsko140QCB64SBa3ai7nvNThezHHA9qGYzIip9gOjyN/AhTEA4M80+3FpbscBrc7FDa08+e2y5cTw7Gdwsmin+QmNlXVOn2rP3jNKMXsFfYS/eSZj5MRjBdzAdstVrUI7i5/OoAAwu0xD6Gou0r6h7/DIsOfltqIA0edgjoGdFTMIU23+0V5D

@dataclass(slots=True, frozen=True)
class AStarNode:
    x: int
    y: int
    cost: int
    f: int
    path: List['PointT']

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

    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

    memory: Set[PointT] = set()
    assert (path := search_memory((0, 0), GOAL, memory)) is not None

    path_dict = {p: i for i, p in enumerate(path)}

    for line in lines:
        x, y = map(int, line.split(','))
        memory.add((x, y))

        if (x, y) in path_dict:
            idx = path_dict[x, y]
            assert idx != 0 and (idx + 1) != len(path)

            bridge = search_memory(path[idx - 1], path[idx + 1], memory)
            if bridge is None:
                path = search_memory((0, 0), GOAL, memory)
                if path is None:
                    break

                path_dict = {p: i for i, p in enumerate(path)}
            else:
                head = idx - 1
                tail = idx + 1
                for (x, y) in bridge:
                    if (x, y) in path_dict:
                        idx = path_dict[x, y]
                        head = min(head, idx)
                        tail = max(tail, idx)

                path = path[:head] + bridge + path[tail+1:]
                path_dict = {p: i for i, p in enumerate(path)}
                assert len(path) == len(path_dict)

    solution = f'{x},{y}'

    tf = time.perf_counter()

    success = solution == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {solution} ({success})')

    return 0 if success else 1


def search_memory(start: PointT, goal: PointT, memory: Set[PointT]) -> List[PointT] | None:
    visited: Set[PointT] = set()

    x, y = start
    heap = [AStarNode(x, y, 0, 0, [start])]
    while len(heap) != 0:
        node = heapq.heappop(heap)

        x = node.x
        y = node.y
        cost = node.cost
        path = node.path

        if (x, y) == goal:
            return path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for (vx, vy) in V:
            x_ = x + vx
            y_ = y + vy

            if 0 <= x_ < WIDTH and 0 <= y_ < HEIGHT and (x_, y_) not in memory and (x_, y_) not in visited:
                cost_ = cost + 1
                h = goal[0]-x_ + goal[1]-y_
                path_ = path + [(x_, y_), ]

                heapq.heappush(heap, AStarNode(x_, y_, cost_, cost_ + h, path_))  # nopep8

    return None


if __name__ == '__main__':
    exit(main())
