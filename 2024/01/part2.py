import os
import sys
import time
from typing import Dict

SOLUTION = 29379307
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


def main() -> int:
    t = time.perf_counter()
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

        left_counter: Dict[int, int] = {}
        right_counter: Dict[int, int] = {}
        for line in lines:
            split = line.split()

            l_value = int(split[0])
            r_value = int(split[1])

            if l_value not in left_counter:
                left_counter[l_value] = 1
            else:
                left_counter[l_value] += 1

            if r_value not in right_counter:
                right_counter[r_value] = 1
            else:
                right_counter[r_value] += 1

    similarity = 0
    for l_value, l_value_counter in left_counter.items():
        if l_value in right_counter:
            similarity += l_value * l_value_counter * right_counter[l_value]

    tf = time.perf_counter()

    success = similarity == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {similarity} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
