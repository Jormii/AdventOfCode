import os
import sys
import time
from typing import Dict, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 156714
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


PointT = Tuple[int, int]
CacheT = Dict[Tuple[int, str, str], int]

N_INTERMEDIATE_ROBOTS = 2

KEYPAD = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    ' ': (3, 0),
    '0': (3, 1),
    'A': (3, 2),
}

DIR_KEYPAD = {
    ' ': (0, 0),
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2),
}


def main() -> int:
    t = time.perf_counter()

    with open(INPUT_FILE) as fd:
        codes = map(lambda ln: ln.strip(), fd.readlines())

    sum_ = 0
    cache: CacheT = {}
    for code in codes:
        length = keypad(code, KEYPAD, cache)
        numerical = int(code.replace('A', ''))

        sum_ += length * numerical

    tf = time.perf_counter()

    success = sum_ == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {sum_} ({success})')

    return 0 if success else 1


def keypad(code: str, pad: Dict[str, PointT], cache: CacheT, robot_idx: int = 0) -> int:
    EMPTY = pad[' ']

    length = 0
    code = f'A{code}'
    for i in range(len(code) - 1):
        button = code[i]
        next_button = code[i + 1]

        if (robot_idx, button, next_button) in cache:
            length += cache[robot_idx, button, next_button]
            continue

        arm = pad[button]
        next_arm = pad[next_button]

        dr = next_arm[0] - arm[0]
        dc = next_arm[1] - arm[1]
        r_button = '^' if dr < 0 else 'v'
        c_button = '<' if dc < 0 else '>'

        if robot_idx == N_INTERMEDIATE_ROBOTS:
            sequence_length = abs(dr) + abs(dc) + 1
        else:
            sequence_length = sys.maxsize

            if dr == 0 and dc == 0:
                a_code = 'A'
                a_length = keypad(a_code, DIR_KEYPAD, cache, robot_idx + 1)

                sequence_length = min(sequence_length, a_length)

            if dr != 0 and (arm[1] != EMPTY[1] or next_arm[0] != EMPTY[0]):
                # Vertical, then horizontal
                v_code = f'{abs(dr)*r_button}{abs(dc)*c_button}A'
                v_length = keypad(v_code, DIR_KEYPAD, cache, robot_idx + 1)

                sequence_length = min(sequence_length, v_length)

            if dc != 0 and (arm[0] != EMPTY[0] or next_arm[1] != EMPTY[1]):
                # Horizontal, then vertical
                h_code = f'{abs(dc)*c_button}{abs(dr)*r_button}A'
                h_length = keypad(h_code, DIR_KEYPAD, cache, robot_idx + 1)

                sequence_length = min(sequence_length, h_length)

        length += sequence_length
        cache[robot_idx, button, next_button] = sequence_length

    return length


if __name__ == '__main__':
    exit(main())
