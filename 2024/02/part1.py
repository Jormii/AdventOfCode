import os
import sys
import time

BIGBOY = False

if not BIGBOY:
    SOLUTION = 306
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 105674
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    safe_reports = 0
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            levels = list(map(int, line.split()))

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
                continue

            is_safe = True
            for i in range(2, len(levels)):
                l0 = lf
                lf = levels[i]

                diff = lf - l0
                if diff < lower_bound or diff > upper_bound:
                    is_safe = False
                    break

            if is_safe:
                safe_reports += 1

    tf = time.perf_counter()

    success = safe_reports == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {safe_reports} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
