import os
import sys
import time
from typing import Dict, Set, Tuple


BIGBOY = False

if not BIGBOY:
    SOLUTION = 'bd,dk,ir,ko,lk,nn,ob,pt,te,tl,uh,wj,yl'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = '-1'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

TriT = Tuple[str, str, str]
GraphT = Dict[str, Set[str]]


def main() -> int:
    t = time.perf_counter()

    graph: GraphT = {}
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            left, right = line.strip().split('-')

            for from_, to_ in ((left, right), (right, left)):
                if from_ not in graph:
                    graph[from_] = {to_}
                else:
                    graph[from_].add(to_)

    R: Set[str] = set()
    P = set(graph.keys())
    X: Set[str] = set()
    maximal_clique = bron_kerbosch(R, P, X, graph)

    solution = ','.join(sorted(maximal_clique))

    tf = time.perf_counter()

    success = solution == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {solution} ({success})')

    return 0 if success else 1


def bron_kerbosch(R: Set[str], P: Set[str], X: Set[str], graph: GraphT) -> Set[str]:
    if len(P) == 0 and len(X) == 0:
        return R

    maximal_clique: Set[str] = set()
    for node in list(P):
        adjacencies = graph[node]

        R_ = R.union((node, ))
        P_ = P.intersection(adjacencies)
        X_ = X.intersection(adjacencies)
        clique = bron_kerbosch(R_, P_, X_, graph)
        if len(clique) > len(maximal_clique):
            maximal_clique = clique

        P.remove(node)
        X.add(node)

    return maximal_clique


if __name__ == '__main__':
    exit(main())
