import os
import sys
import time
from typing import Dict, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 204022
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    BLINKS = 75

    t = time.perf_counter()

    stones: Dict[int, int] = {}
    with open(INPUT_FILE) as fd:
        for stone in map(int, fd.readline().split()):
            if stone not in stones:
                stones[stone] = 1
            else:
                stones[stone] += 1

    # NOTE: I swear Python is making me dumber...

    read_dict = stones
    update_dict: Dict[int, int] = {}
    cache: Dict[int, Tuple[int, int]] = {}
    for _ in range(BLINKS):
        update_dict.clear()

        for stone, n_stones in read_dict.items():
            if stone == 0:
                _update(update_dict, stone + 1, n_stones)
            elif stone in cache:
                left, right = cache[stone]
                _update(update_dict, left, n_stones)
                _update(update_dict, right, n_stones)
            else:
                stone_str = str(stone)

                if (len(stone_str) % 2) != 0:
                    _update(update_dict, 2024*stone, n_stones)
                else:
                    half = len(stone_str) // 2
                    left = int(stone_str[half:])
                    right = int(stone_str[:half])

                    cache[stone] = (left, right)
                    _update(update_dict, left, n_stones)
                    _update(update_dict, right, n_stones)

        read_dict, update_dict = update_dict, read_dict

    n_stones = sum(v for v in read_dict.values())

    tf = time.perf_counter()

    success = n_stones == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {n_stones} ({success})')

    return 0 if success else 1


def _update(d: Dict[int, int], stone: int, n_stones: int) -> None:
    if stone not in d:
        d[stone] = n_stones
    else:
        d[stone] += n_stones


if __name__ == '__main__':
    exit(main())
