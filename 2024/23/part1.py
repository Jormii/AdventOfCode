import os
import sys
import time
from typing import Dict, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 1306
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

TriT = Tuple[str, str, str]
GraphT = Dict[str, Set[str]]


def main() -> int:
    t = time.perf_counter()

    ts: Set[str] = set()
    graph: GraphT = {}
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            left, right = line.strip().split('-')

            for from_, to_ in ((left, right), (right, left)):
                if from_[0] == 't':
                    ts.add(from_)

                if from_ not in graph:
                    graph[from_] = {to_}
                else:
                    graph[from_].add(to_)

    triangles: Set[TriT] = set()
    for from_ in ts:
        for to_ in graph[from_]:
            triangles.update(get_triangles(from_, to_, graph))

    tf = time.perf_counter()

    success = len(triangles) == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {len(triangles)} ({success})')

    return 0 if success else 1


def get_triangles(from_: str, to_: str, graph: GraphT) -> Set[TriT]:
    from_edges = graph[from_]
    to_edges = graph[to_]

    triangles: Set[TriT] = set()
    for node in from_edges:
        if node in to_edges and node != to_:
            tri = tuple(sorted((from_, to_, node)))
            triangles.add(tri)  # type: ignore[arg-type]

    return triangles


if __name__ == '__main__':
    exit(main())
