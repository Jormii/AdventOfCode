import os
import sys
import time
from typing import Dict, Set

BIGBOY = False

if not BIGBOY:
    SOLUTION = 6179
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
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

            left = int(line[:2])
            right = int(line[3:5])

            if right not in rules_inv:
                rules_inv[right] = {left}
            else:
                rules_inv[right].add(left)

        for line in lines[i+1:]:
            page_numbers = list(map(int, line.strip().split(',')))

            ordered = True
            for i in range(len(page_numbers) - 1):
                left = page_numbers[i]
                right = page_numbers[i + 1]
                if left in rules_inv and right in rules_inv[left]:
                    ordered = False
                    break

            if ordered:
                continue

            degree: Dict[int, int] = {}
            # NOTE: -1 for each output, +1 for each input

            for page_number in page_numbers:
                if page_number not in rules_inv:
                    continue

                for other_page_number in page_numbers:
                    if other_page_number not in rules_inv[page_number]:
                        continue

                    if page_number not in degree:
                        degree[page_number] = 1
                    else:
                        degree[page_number] += 1

                    if other_page_number not in degree:
                        degree[other_page_number] = -1
                    else:
                        degree[other_page_number] -= 1

            degree = dict(sorted(degree.items(), key=lambda kv: kv[1]))
            total += list(degree.keys())[len(degree) // 2]

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
