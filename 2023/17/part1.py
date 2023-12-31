import os
import bisect
import numpy as np
from typing import List, TypeVar, Union

T = TypeVar("T")
OptT = Union[T, None]

SOLUTION = 886

STRAIGHT_LINE_LIMIT = 3


class DijkstraNode:

    def __init__(self, row: int, column: int, vx: int, vy: int,
                 cost: int) -> None:
        self.row = row
        self.column = column
        self.vx, self.vy = vx, vy

        self.cost = cost

    def __lt__(self, o) -> bool:
        return self.cost < o.cost


def main() -> int:
    input_path = os.path.join(os.path.split(__file__)[0], "input.txt")

    fd = open(input_path, "r")

    heat_map: List[List[int]] = []

    l = fd.readline().strip()
    while len(l) != 0:
        heat_map.append(parse_row(l))

        l = fd.readline().strip()

    heat_map = np.array(heat_map)
    solution = dijkstra_search(heat_map)

    fd.close()

    success = solution == SOLUTION
    print(f"Solution: {solution} ({success})")

    return success


def parse_row(line: str) -> List[int]:
    return [int(c) for c in line]


def dijkstra_search(heat_map: np.ndarray) -> int:
    V_MAPPING = {
        (0, -1): 0,
        (-1, 0): 1,
        (0, 1): 2,
        (1, 0): 3
    }

    width = heat_map.shape[1]
    height = heat_map.shape[0]
    shape = (height, width, len(V_MAPPING))

    EMPTY = 10 * width * height

    row = 0
    column = 0
    dijkstra = np.full(shape, EMPTY)
    queue: List[DijkstraNode] = [
        DijkstraNode(row, column, 1, 0, 0),
        DijkstraNode(row, column, 0, 1, 0),
    ]
    while len(queue) != 0:
        node = queue.pop(0)
        if (node.row + 1) == height and (node.column + 1) == width:
            return node.cost

        v_idx = V_MAPPING[(node.vx, node.vy)]
        cost = dijkstra[node.row, node.column, v_idx]

        if cost != EMPTY:
            continue

        dijkstra[node.row, node.column, v_idx] = node.cost

        V = [
            (node.vy, node.vx),
            (-node.vy, -node.vx),
        ]
        for (vx, vy) in V:
            v_idx = V_MAPPING[(vx, vy)]

            row = node.row
            column = node.column
            acc_cost = node.cost
            for i in range(STRAIGHT_LINE_LIMIT):
                row += vy
                column += vx
                if not (row >= 0 and row < height and column >= 0 and column < width):
                    break

                acc_cost += heat_map[row, column]
                if dijkstra[row, column, v_idx] == EMPTY:
                    bisect.insort_left(
                        queue, DijkstraNode(row, column, vx, vy, acc_cost))


if __name__ == "__main__":
    exit(main())
