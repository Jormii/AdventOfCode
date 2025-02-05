from __future__ import annotations
import os
import sys
import time
import heapq
from collections import defaultdict

BIGBOY = True

if not BIGBOY:
    SOLUTION = 6408966547049
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 70351090993107482
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


class File:
    id: int
    off: int
    size: int

    __slots__ = ['id', 'off', 'size']

    def __init__(self, id: int, off: int, size: int) -> None:
        self.id = id
        self.off = off
        self.size = size


class FreeSpace:
    off: int
    size: int

    __slots__ = ['off', 'size']

    def __init__(self, off: int, size: int) -> None:
        self.off = off
        self.size = size


def main() -> int:

    t = time.perf_counter()

    with open(INPUT_FILE) as f:
        rawinput = f.read()

    lengths = [int(num) for num in rawinput]

    filled_grid = {}  # ID: start,length
    gaps = defaultdict(lambda: [])  # length: start

    cur_pos = 0
    for i, num in enumerate(lengths):
        if i % 2 == 0:
            filled_grid[i//2] = [cur_pos, num]
        else:
            if num > 0:
                heapq.heappush(gaps[num], cur_pos)
        cur_pos += num

    for i in sorted(filled_grid.keys(), reverse=True):
        file_start_pos, file_len = filled_grid[i]
        possible_gaps = sorted([[gaps[gap_len][0], gap_len]
                               for gap_len in gaps if gap_len >= file_len])
        if possible_gaps:
            gap_start_pos, gap_len = possible_gaps[0]
            if file_start_pos > gap_start_pos:
                filled_grid[i] = [gap_start_pos, file_len]
                remaining_gap_len = gap_len-file_len
                heapq.heappop(gaps[gap_len])
                if not gaps[gap_len]:
                    del gaps[gap_len]
                if remaining_gap_len:
                    heapq.heappush(gaps[remaining_gap_len],
                                   gap_start_pos+file_len)

    checksum = sum(num*(start*length+(length*(length-1))//2) for num, (start, length)
                   in filled_grid.items())  # (start) + (start+1) + ... + (start+length-1)

    tf = time.perf_counter()

    success = checksum == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {checksum} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
