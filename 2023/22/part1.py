import os
import re
import numpy as np
from typing import List, Set, TypeVar, Union

T = TypeVar("T")
OptT = Union[T, None]

SOLUTION = 411


class Snapshot:

    def __init__(self, x0: int, y0: int, z0: int, xf: int, yf: int, zf: int) -> None:
        self.x0, self.xf = x0, xf
        self.y0, self.yf = y0, yf
        self.z0, self.zf = z0, zf

        self.supports: Set[Snapshot] = set()
        self.supported_by: Set[Snapshot] = set()


class Support:

    def __init__(self) -> None:
        self.z = 0
        self.snapshot: OptT[Snapshot] = None


def main() -> int:
    input_path = os.path.join(os.path.split(__file__)[0], "input.txt")

    fd = open(input_path, "r")

    width = 0
    depth = 0
    snapshots: List[Snapshot] = []

    l = fd.readline().strip()
    while len(l) != 0:
        snapshot = parse_row(l)
        width = max(width, snapshot.xf + 1)
        depth = max(depth, snapshot.yf + 1)

        snapshots.append(snapshot)

        l = fd.readline().strip()

    settle(snapshots, width, depth)
    solution = disintegrate(snapshots)

    fd.close()

    success = solution == SOLUTION
    print(f"Solution: {solution} ({success})")

    return success


def parse_row(line: str) -> Snapshot:
    REGEX = rf"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)"

    match = re.search(REGEX, line)
    return Snapshot(*[int(g) for g in match.groups()])


def settle(snapshots: List[Snapshot], width: int, depth: int) -> None:
    supports = np.ndarray((width, depth), Support)
    for x in range(width):
        for y in range(depth):
            supports[x, y] = Support()

    snapshots.sort(key=lambda s: s.z0)
    for snapshot in snapshots:
        z = 0
        for x in range(snapshot.x0, snapshot.xf + 1):
            for y in range(snapshot.y0, snapshot.yf + 1):
                support: Support = supports[x, y]

                if support.z > z:
                    z = support.z

                    for supported_by in snapshot.supported_by:
                        supported_by.supports.remove(snapshot)
                    snapshot.supported_by.clear()

                if support.z == z and support.snapshot is not None:
                    support.snapshot.supports.add(snapshot)
                    snapshot.supported_by.add(support.snapshot)

        settled_z = z + (snapshot.zf - snapshot.z0 + 1)
        for x in range(snapshot.x0, snapshot.xf + 1):
            for y in range(snapshot.y0, snapshot.yf + 1):
                support: Support = supports[x, y]

                support.z = settled_z
                support.snapshot = snapshot


def disintegrate(snapshots: List[Snapshot]) -> int:
    disintegrate_count = 0
    for snapshot in snapshots:
        can_disintegrate = True
        for supported in snapshot.supports:
            can_disintegrate &= len(supported.supported_by) != 1

        disintegrate_count += can_disintegrate

    return disintegrate_count


if __name__ == "__main__":
    exit(main())
