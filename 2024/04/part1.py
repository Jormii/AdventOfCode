import os
import sys
import time
from typing import List

SOLUTION = 2378
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


MatrixT = List[List[int]]

XMAS = [ord('X'), ord('M'), ord('A'), ord('S')]
XMAS_REVERSED = [ord('S'), ord('A'), ord('M'), ord('X')]


def main() -> int:
    t = time.perf_counter()

    total = 0
    matrix: MatrixT = []
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            matrix.append(list(map(ord, line)))

    total += find(matrix)
    total += find(transpose(matrix))
    total += find(transpose(roll_left(matrix)))
    total += find(transpose(roll_right(matrix)))

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


def find(matrix: MatrixT) -> int:
    total = 0

    rows = len(matrix)
    columns = len(matrix[0])
    for r in range(rows):
        for c in range(columns):
            element = matrix[r][c]

            if element == XMAS[0]:
                total += matrix[r][c:c+len(XMAS)] == XMAS
            elif element == XMAS_REVERSED[0]:
                total += matrix[r][c:c+len(XMAS_REVERSED)] == XMAS_REVERSED

    return total


def transpose(matrix: MatrixT) -> MatrixT:
    rows = len(matrix)
    columns = len(matrix[0])

    transposed: MatrixT = []
    transposed.extend([0]*rows for _ in range(columns))

    for r in range(rows):
        for c in range(columns):
            transposed[c][r] = matrix[r][c]

    return transposed


def roll_left(matrix: MatrixT) -> MatrixT:
    rows = len(matrix)
    columns = len(matrix[0])

    rolled: MatrixT = []
    for r in range(rows):
        rolled.append([0] * columns)

        for c in range(columns):
            rolled[r][c] = matrix[r][(c + r) % columns]

    return rolled


def roll_right(matrix: MatrixT) -> MatrixT:
    rows = len(matrix)
    columns = len(matrix[0])

    rolled: MatrixT = []
    for r in range(rows):
        rolled.append([0] * columns)

        for c in range(columns):
            rolled[r][c] = matrix[r][c - r]

    return rolled


if __name__ == '__main__':
    exit(main())
