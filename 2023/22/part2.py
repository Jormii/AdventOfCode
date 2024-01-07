import os
import re
import numpy as np
from typing import List, Set, Tuple, TypeVar, Union

T = TypeVar("T")
OptT = Union[T, None]

SOLUTION = 47671


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

    return 0 if success else 1


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
    total = 0
    for snapshot in snapshots:
        chain_reaction = remove(snapshot, set())
        total += sum(t[0] for t in chain_reaction)

    return total


def remove(snapshot: Snapshot, removed: Set[Snapshot]) -> List[Tuple[bool, Snapshot, Snapshot]]:
    chain: List[Tuple[bool, Snapshot, Snapshot]] = []

    removed.add(snapshot)
    is_first = len(removed) == 1

    for supported in snapshot.supports:
        supported.supported_by.remove(snapshot)

        falls = len(supported.supported_by) == 0
        chain.append((falls, snapshot, supported))

    for (falls, _, supported) in chain:
        if falls and supported not in removed:
            chain.extend(remove(supported, removed))

    if is_first:
        for (_, support, supported) in chain:
            supported.supported_by.add(support)

    return chain


if __name__ == "__main__":
    exit(main())
