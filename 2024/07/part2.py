import os
import re
import sys
import time

BIGBOY = False

if not BIGBOY:
    SOLUTION = 116094961956019
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

ADD = 0
MULT = 1
CONCAT = 2

# TODO: No combinations


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
            operators = [ADD] * op_count
            combinations = 3 ** op_count

            for _ in range(combinations):
                it_value = numbers[0]

                for i in range(len(numbers) - 1):
                    op = operators[i]
                    operand = numbers[i + 1]

                    if op == ADD:
                        it_value += operand
                    elif op == MULT:
                        it_value *= operand
                    elif op == CONCAT:
                        it_value = int(f'{it_value}{operand}')

                if it_value == value:
                    total += value
                    break

                for i in range(len(operators)):
                    if operators[i] == CONCAT:
                        operators[i] = ADD
                    else:
                        operators[i] += 1
                        break

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
