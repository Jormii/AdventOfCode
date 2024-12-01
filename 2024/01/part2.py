import os
import re
from typing import Dict, List, Tuple

SOLUTION = 29379307
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


def main() -> int:
    left, right = read_input()

    appearance: Dict[int, int] = {}
    for r_value in right:
        if r_value not in appearance:
            appearance[r_value] = 1
        else:
            appearance[r_value] += 1

    similarity = 0
    for l_value in left:
        if l_value in appearance:
            similarity += l_value * appearance[l_value]

    success = similarity == SOLUTION
    print(f'Solution: {similarity} ({success})')

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
