import os
import re
import sys
import time
from typing import List, Set, Tuple

SOLUTION = 1796
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


MatrixT = List[List[int]]
FindRetT = List[Tuple[int, int]]

REGEX = r'(?=(MAS|SAM))'
PATTERN = re.compile(REGEX)


def main() -> int:
    t = time.perf_counter()

    total = 0
    matrix: MatrixT = []
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            matrix.append(list(map(ord, line)))

    rolled_left_T, rolled_right_T = roll_then_transpose(matrix)

    left_found = find(rolled_left_T)
    right_found = find(rolled_right_T)

    columns = len(matrix[0])
    centers: Set[Tuple[int, int]] = set()
    for (c, r) in left_found:
        # 'A'^T ("for (c, r) in ..." instead of "for (r, c) in ...") and unroll
        c = (c + r) % columns

        centers.add((r, c))

    for (c, r) in right_found:
        # 'A'^T ("for (c, r) in ..." instead of "for (r, c) in ...") and unroll
        c = (c - r) % columns

        if (r, c) in centers:
            total += 1

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


def find(matrix: MatrixT) -> FindRetT:
    found: FindRetT = []

    for r, row in enumerate(matrix):
        line = bytes(row).decode()
        for match in PATTERN.finditer(line):
            span = match.span()

            c = span[0]
            found.append((r, c + 1))

    return found


def roll_then_transpose(matrix: MatrixT) -> Tuple[MatrixT, MatrixT]:
    rows = len(matrix)
    columns = len(matrix[0])

    rolled_left_T = [[0]*rows for _ in range(columns)]
    rolled_right_T = [[0]*rows for _ in range(columns)]

    for r in range(rows):
        for c in range(columns):
            rolled_left_T[c][r] = matrix[r][(c + r) % columns]
            rolled_right_T[c][r] = matrix[r][c - r]

    return rolled_left_T, rolled_right_T


if __name__ == '__main__':
    exit(main())
