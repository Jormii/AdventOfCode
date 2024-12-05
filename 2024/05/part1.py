import os
import sys
import time
from typing import Dict, Set

BIGBOY = False

if not BIGBOY:
    SOLUTION = 4578
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 14346279
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

RulesT = Dict[int, Set[int]]


def main() -> int:
    t = time.perf_counter()

    total = 0
    rules_inv: RulesT = {}  # Instead of "A before B", "B after A"
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()
        for i, line in enumerate(lines):
            if line == '\n':
                break

            left, right = map(int, line.split('|'))

            if right not in rules_inv:
                rules_inv[right] = {left}
            else:
                rules_inv[right].add(left)

        for line in lines[i+1:]:
            page_numbers = list(map(int, line.split(',')))

            ordered = True
            for i in range(len(page_numbers) - 1):
                left = page_numbers[i]
                right = page_numbers[i + 1]
                if left in rules_inv and right in rules_inv[left]:
                    ordered = False
                    break

            if ordered:
                total += page_numbers[len(page_numbers) // 2]

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
