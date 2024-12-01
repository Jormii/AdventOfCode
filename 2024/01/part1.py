import os
import re
from typing import List, Tuple

SOLUTION = 3246517
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


def main() -> int:
    left, right = read_input()

    left.sort()
    right.sort()

    distance = 0
    for l_value, r_value in zip(left, right, strict=True):
        distance += abs(l_value - r_value)

    success = distance == SOLUTION
    print(f'Solution: {distance} ({success})')

    return 0 if success else 1


def read_input() -> Tuple[List[int], List[int]]:
    REGEX = r'^(\d+) +(\d+)$'

    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

        left = [0] * len(lines)
        right = [0] * len(lines)
        for i, line in enumerate(lines):
            search = re.search(REGEX, line)
            assert search is not None

            left[i] = int(search.group(1))
            right[i] = int(search.group(2))

    return left, right


if __name__ == '__main__':
    exit(main())
