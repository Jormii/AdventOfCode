import os
import re
import sys
import time
from typing import List, Tuple

SOLUTION = 2378
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


MatrixT = List[List[int]]

REGEX = r'(?=(XMAS|SAMX))'
PATTERN = re.compile(REGEX)


def main() -> int:
    t = time.perf_counter()

    total = 0
    matrix: MatrixT = []
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            matrix.append(list(map(ord, line)))

    matrix_T = transpose(matrix)
    rolled_left_T, rolled_right_T = roll_then_transpose(matrix)

    total += find(matrix)
    total += find(matrix_T)
    total += find(rolled_left_T)
    total += find(rolled_right_T)

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


def find(matrix: MatrixT) -> int:
    total = 0

    for row in matrix:
        line = bytes(row).decode()
        total += len(PATTERN.findall(line))

    return total


def transpose(matrix: MatrixT) -> MatrixT:
    rows = len(matrix)
    columns = len(matrix[0])

    transposed = [[0]*rows for _ in range(columns)]

    for r in range(rows):
        for c in range(columns):
            transposed[c][r] = matrix[r][c]

    return transposed


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
