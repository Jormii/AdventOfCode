import os
import re
import sys
import time

BIGBOY = False

if not BIGBOY:
    SOLUTION = 267566105056
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    REGEX = r'^(\d+): (.*)$'
    PATTERN = re.compile(REGEX)

    total = 0
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            assert (search := PATTERN.search(line)) is not None

            value = int(search.group(1))
            numbers = list(map(int, search.group(2).split()))

            op_count = len(numbers) - 1
            combinations = 1 << op_count

            for mask in range(combinations):
                it_value = numbers[0]

                for i in range(len(numbers) - 1):
                    flag = 1 << i
                    operand = numbers[i + 1]

                    if mask & flag:
                        it_value += operand
                    else:
                        it_value *= operand

                if it_value == value:
                    total += value
                    break
                elif it_value < value and mask == 0:
                    break

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
