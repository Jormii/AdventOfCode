import os
import re
import sys
import time
import math

BIGBOY = False

if not BIGBOY:
    SOLUTION = 93866170395343
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    A_COST = 3
    B_COST = 1
    BUTTON_REGEX = r'Button [AB]: X\+(\d+), Y\+(\d+)'
    PRIZE_REGEX = r'Prize: X=(\d+), Y=(\d+)'

    BUTTON_PATTERN = re.compile(BUTTON_REGEX)
    PRIZE_PATTERN = re.compile(PRIZE_REGEX)

    tokens = 0
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()
        for i in range(0, len(lines), 4):
            A = BUTTON_PATTERN.search(lines[i])
            B = BUTTON_PATTERN.search(lines[i + 1])
            prize = PRIZE_PATTERN.search(lines[i + 2])

            assert A is not None
            assert B is not None
            assert prize is not None

            a1, a2 = map(int, A.group(1, 2))
            b1, b2 = map(int, B.group(1, 2))
            c1, c2 = map(int, prize.group(1, 2))

            c1 += 10000000000000
            c2 += 10000000000000

            den = a1*b2 - b1*a2
            a_dec, a_presses = math.modf((c1*b2 - b1*c2) / den)
            b_dec, b_presses = math.modf((a1*c2 - a2*c1) / den)

            if a_dec == 0 and b_dec == 0:
                tokens += A_COST*int(a_presses) + B_COST*int(b_presses)

    tf = time.perf_counter()

    success = tokens == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {tokens} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
