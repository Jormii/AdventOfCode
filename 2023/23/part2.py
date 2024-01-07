import os
from typing import Dict, List, Set, Tuple, TypeVar, Union

T = TypeVar("T")
OptT = Union[T, None]

SOLUTION = 6406


class Node:

    def __init__(self, row: int, column: int,
                 steps: int, visited: Set[Tuple[int, int]]) -> None:
        self.row = row
        self.column = column

        self.steps = steps
        self.visited = visited


def main() -> int:
    input_path = os.path.join(os.path.split(__file__)[0], "input.txt")

    fd = open(input_path, "r")

    trails: List[List[str]] = []
    l = fd.readline().strip()
    while len(l) != 0:
        trails.append(parse_row(l))

        l = fd.readline().strip()

    graph = build_graph(trails)
    solution = longest_hike(trails, graph)

    fd.close()

    success = solution == SOLUTION
    print(f"Solution: {solution} ({success})")

    return 0 if success else 1


def parse_row(line: str) -> List[str]:
    return [c for c in line]


def build_graph(trails: List[List[str]]) -> Dict[Tuple[int, int], Dict[Tuple[int, int], int]]:
    START_ROW = 0
    START_COLUMN = 1
    V = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    height = len(trails)
    width = len(trails[0])

    exit_row = height - 1
    exit_column = width - 2

    graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]] = {
        (START_ROW, START_COLUMN): {},
        (exit_row, exit_column): {}
    }

    queue: List[Tuple[int, int, int, int]] = [
        (START_ROW, START_COLUMN, START_ROW, START_COLUMN),
        (exit_row, exit_column, exit_row, exit_column)
    ]
    while len(queue) != 0:
        row, column, start_row, start_column = queue.pop(0)
        visited: Set[Tuple[int, int]] = set([(start_row, start_column)])

        steps = 0
        if not (row == start_row and column == start_column):
            steps += 1

        explore = True
        while explore:
            steps += 1
            visited.add((row, column))

            neighbors: List[Tuple[int, int]] = []
            for (vx, vy) in V:
                n_row = row + vy
                n_column = column + vx

                if not (n_row >= 0 and n_row < height and n_column >= 0 and n_column < width) \
                        or (n_row, n_column) in visited:
                    continue

                tile = trails[n_row][n_column]
                if tile != '#':
                    neighbors.append((n_row, n_column))

            if len(neighbors) == 0:
                explore = False
            elif len(neighbors) == 1:
                row, column = neighbors[0]
            else:
                explore = False

                if (row, column) not in graph:
                    graph[(row, column)] = {}
                if (start_row, start_column) not in graph:
                    graph[(start_row, start_column)] = {}

                if (row, column) not in graph[(start_row, start_column)]:
                    graph[(row, column)][(start_row, start_column)] = steps
                    graph[(start_row, start_column)][(row, column)] = steps

                    for (n_row, n_column) in neighbors:
                        queue.append((n_row, n_column, row, column))

    return graph


def longest_hike(trails: List[List[str]],
                 graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]]) -> int:
    START_ROW = 0
    START_COLUMN = 1

    height = len(trails)
    width = len(trails[0])

    exit_row = height - 1
    exit_column = width - 2

    longest = 0
    queue = [
        Node(START_ROW, START_COLUMN, 0, set([(START_ROW, START_COLUMN)]))
    ]
    while len(queue) != 0:
        node = queue.pop(0)
        if node.row == exit_row and node.column == exit_column:
            longest = max(longest, node.steps)
            continue

        for (row, column), cost in graph[(node.row, node.column)].items():
            if (row, column) not in node.visited:
                visited = set(node.visited)
                visited.add((row, column))
                steps = node.steps + cost - 1

                queue.insert(0, Node(row, column, steps, visited))

    return longest


if __name__ == "__main__":
    exit(main())
