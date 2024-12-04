import os
import sys
import time
from typing import List, Set, Tuple

SOLUTION = 1796
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


MatrixT = List[List[int]]
FindRetT = List[Tuple[int, int]]

MAS = [ord('M'), ord('A'), ord('S')]
MAS_REVERSED = [ord('S'), ord('A'), ord('M')]


def main() -> int:
    t = time.perf_counter()

    total = 0
    matrix: MatrixT = []
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            matrix.append(list(map(ord, line)))

    left_found = find(transpose(roll_left(matrix)))
    right_found = find(transpose(roll_right(matrix)))

    rows = len(matrix)
    columns = len(matrix[0])
    crosses: Set[Tuple[int, int]] = set()
    for (c, r) in left_found:
        # 'A'^T ("for (c, r) in ..." instead of "for (r, c) in ...") and unroll
        r %= rows
        c = (c + r) % columns

        crosses.add((r, c))

    for (c, r) in right_found:
        # 'A'^T ("for (c, r) in ..." instead of "for (r, c) in ...") and unroll
        r %= rows
        c = (c - r) % columns

        if (r, c) in crosses:
            total += 1
        else:
            crosses.add((r, c))

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


def find(matrix: MatrixT) -> FindRetT:
    found: FindRetT = []

    rows = len(matrix)
    columns = len(matrix[0])
    for r in range(rows):
        for c in range(columns):
            element = matrix[r][c]

            if element == MAS[0] \
                    and matrix[r][c:c+len(MAS)] == MAS:
                found.append((r, c + 1))
            elif element == MAS_REVERSED[0]\
                    and matrix[r][c:c+len(MAS_REVERSED)] == MAS_REVERSED:
                found.append((r, c + 1))

    return found


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
