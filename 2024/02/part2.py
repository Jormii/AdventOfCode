import os
import sys
import time
from typing import List
from enum import IntEnum

SOLUTION = 366
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


class Tendency(IntEnum):
    INC = 0
    DEC = 1


DIFF_LEAST = 1
DIFF_MOST = 3


def main() -> int:
    t = time.perf_counter()

    safe_reports = 0
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            levels = list(map(int, line.split()))

            if are_safe(levels):
                safe_reports += 1
            else:
                for i in range(len(levels)):
                    copy = list(levels)
                    del copy[i]
                    if are_safe(copy):
                        safe_reports += 1
                        break

    tf = time.perf_counter()

    success = safe_reports == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {safe_reports} ({success})')

    return 0 if success else 1


def are_safe(levels: List[int]) -> bool:
    l0 = levels[0]
    lf = levels[1]
    difference = abs(lf - l0)
    tendency = Tendency.DEC if l0 > lf else Tendency.INC
    if difference < DIFF_LEAST or difference > DIFF_MOST:
        return False

    for i in range(1, len(levels) - 1):
        l0 = levels[i]
        lf = levels[i + 1]

        difference = abs(lf - l0)
        ith_tendency = Tendency.DEC if l0 > lf else Tendency.INC
        if ith_tendency != tendency \
                or difference < DIFF_LEAST or difference > DIFF_MOST:
            return False

    return True


if __name__ == '__main__':
    exit(main())
