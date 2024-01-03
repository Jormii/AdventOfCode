import os
from typing import List, Set, Tuple, TypeVar, Union

T = TypeVar("T")
OptT = Union[T, None]

SOLUTION = 2018


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

    solution = longest_hike(trails)

    fd.close()

    success = solution == SOLUTION
    print(f"Solution: {solution} ({success})")

    return success


def parse_row(line: str) -> List[str]:
    return [c for c in line]


def longest_hike(trails: List[List[str]]) -> int:
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

    longest = 0
    queue = [
        Node(START_ROW, START_COLUMN, 0, set([(START_ROW, START_COLUMN)]))
    ]
    while len(queue) != 0:
        node = queue.pop(0)
        if node.row == exit_row and node.column == exit_column:
            longest = max(longest, node.steps)
            continue

        for (vx, vy) in V:
            row = node.row + vy
            column = node.column + vx
            if not (row >= 0 and row < height and column >= 0 and column < width) \
                    or (row, column) in node.visited:
                continue

            add = False
            slope = False
            tile = trails[row][column]
            if tile == '#':
                pass
            elif tile == '.':
                add = True
            elif tile == 'v' and vy == 1:
                add = True
                slope = True

                row += vy
            elif tile == '^' and vy == -1:
                add = True
                slope = True

                row += vy
            elif tile == '>' and vx == 1:
                add = True
                slope = True

                column += vx
            elif tile == '<' and vx == -1:
                add = True
                slope = True

                column += vx

            if add:
                visited = set(node.visited)
                visited.add((row, column))
                steps = node.steps + 1 + slope

                queue.append(Node(row, column, steps, visited))

    return longest


if __name__ == "__main__":
    exit(main())
