import os
import sys
import time
from typing import List

BIGBOY = False

if not BIGBOY:
    SOLUTION = 366
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 140773
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    safe_reports = 0
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            levels = list(map(int, line.split()))

            l0 = levels[0]
            lm = levels[1]
            lf = levels[2]

            if l0 == lm:
                del levels[1]
                is_safe = are_safe(levels)
            elif lm == lf:
                del levels[2]
                is_safe = are_safe(levels)
            elif l0 == lf:
                # NOTE: A diagram helps
                if l0 < lm:
                    if lm < levels[3]:
                        del levels[2]
                    else:
                        del levels[0]
                else:
                    if lm < levels[3]:
                        del levels[0]
                    else:
                        del levels[2]

                is_safe = are_safe(levels)
            elif l0 < lm and lm < lf:
                is_safe = are_safe_with_discard(levels)
            elif l0 > lm and lm > lf:
                is_safe = are_safe_with_discard(levels)
            elif True:
                # NOTE: Head is "skewed" => Either of the three first is wrong
                level = levels.pop(2)
                for i in reversed(range(-1, 2)):
                    if (is_safe := are_safe(levels)):
                        break

                    level, levels[i] = levels[i], level

            if is_safe:
                safe_reports += 1

    tf = time.perf_counter()

    success = safe_reports == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {safe_reports} ({success})')

    return 0 if success else 1


def are_safe(levels: List[int]) -> bool:
    l0 = levels[0]
    lf = levels[1]

    if l0 < lf:
        lower_bound = 1
        upper_bound = 3
    else:
        lower_bound = -3
        upper_bound = -1

    diff = lf - l0
    if diff < lower_bound or diff > upper_bound:
        return False

    for i in range(2, len(levels)):
        l0 = lf
        lf = levels[i]

        diff = lf - l0
        if diff < lower_bound or diff > upper_bound:
            return False

    return True


def are_safe_with_discard(levels: List[int]) -> bool:
    l0 = levels[0]
    lf = levels[1]

    if l0 < lf:
        lower_bound = 1
        upper_bound = 3
    else:
        lower_bound = -3
        upper_bound = -1

    for i in range(len(levels) - 1):
        l0 = levels[i]
        lf = levels[i + 1]

        diff = lf - l0
        if diff < lower_bound or diff > upper_bound:
            if (i + 2) == len(levels):
                return True  # NOTE: True because last value is the wrong one

            pass                # levels = [..., l0, lf, ...]
            del levels[i]       # levels = [..., lf, ...]

            if _are_safe_with_discard(levels, i - 1, lower_bound, upper_bound):
                return True

            levels[i] = l0      # levels = [..., l0, ...]
            if _are_safe_with_discard(levels, i - 1, lower_bound, upper_bound):
                return True

            return False

    return True


def _are_safe_with_discard(
        levels: List[int],
        begin_idx: int,
        lower_bound: int,
        upper_bound: int
) -> bool:
    begin_idx = max(0, begin_idx)
    for i in range(begin_idx, len(levels) - 1):
        l0 = levels[i]
        lf = levels[i + 1]

        diff = lf - l0
        if diff < lower_bound or diff > upper_bound:
            return False

    return True


if __name__ == '__main__':
    exit(main())
