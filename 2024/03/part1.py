import os
import re
import sys
import time

BIGBOY = False

if not BIGBOY:
    SOLUTION = 179571322
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 1491954950936
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    MUL_REGEX = r'mul\((\d{1,3}),(\d{1,3})\)'
    MUL_PATTERN = re.compile(MUL_REGEX)

    total = 0
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            for mul_inst in MUL_PATTERN.finditer(line):
                left = int(mul_inst.group(1))
                right = int(mul_inst.group(2))

                total += left * right

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
