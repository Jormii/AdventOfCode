import os
import re
import heapq
from math import inf
from typing import Dict, List, Set, Tuple, TypeVar, Union

T = TypeVar("1")
OptT = Union[T, None]

GraphT = Dict[str, Dict[str, int]]

SOLUTION = 555702

DISCONNECTIONS = 3


def main() -> int:
    input_path = os.path.join(os.path.split(__file__)[0], "input.txt")

    fd = open(input_path, "r")

    graph: GraphT = {}

    l = fd.readline().strip()
    while len(l) != 0:
        parse_row(l, graph)

        l = fd.readline().strip()

    fd.close()

    og_graph_size = len(graph)
    _, phase_idx, contractions = stoer_wagner(graph)
    partition = reconstruct(phase_idx, contractions)

    solution = len(partition) * (og_graph_size - len(partition))

    success = solution == SOLUTION
    print(f"Solution: {solution} ({success})")

    return 0 if success else 1


def parse_row(line: str, out_graph: GraphT) -> None:
    REGEX = r"\w+"

    vertices = re.findall(REGEX, line)

    vertex = vertices[0]
    adjacency = vertices[1:]

    if vertex not in out_graph:
        out_graph[vertex] = {}

    for adjacent in adjacency:
        if adjacent not in out_graph:
            out_graph[adjacent] = {}

        out_graph[vertex][adjacent] = 1
        out_graph[adjacent][vertex] = 1


def stoer_wagner(out_graph: GraphT) -> Tuple[int, int, List[Tuple[str, str]]]:
    min_cut = inf
    best_phase_idx = 0
    contractions: List[Tuple[str, str]] = []

    phase_idx = 0
    root = next(iter(out_graph.keys()))
    while len(out_graph) != 1 and min_cut != DISCONNECTIONS:
        cut_of_phase, contraction = min_cut_phase(root, out_graph)

        if cut_of_phase < min_cut:
            min_cut = cut_of_phase
            best_phase_idx = phase_idx

        phase_idx += 1
        contractions.append(contraction)

    return min_cut, best_phase_idx, contractions


def min_cut_phase(root: str, out_graph: GraphT) -> Tuple[int, Tuple[str, str]]:
    heap: List[Tuple[int, str]] = []
    priority: Dict[str, int] = {v: 0 for v in out_graph.keys()}

    for vertex, weight in out_graph[root].items():
        priority[vertex] += weight
        heapq.heappush(heap, (-priority[vertex], vertex))

    A: List[str] = [root]
    unvisited: Set[str] = set(out_graph.keys()).difference(A)
    while len(A) != len(out_graph):
        _, vertex = heapq.heappop(heap)
        if vertex not in unvisited:
            continue

        A.append(vertex)
        unvisited.remove(vertex)

        for adjacent, weight in out_graph[vertex].items():
            if adjacent in unvisited:
                priority[adjacent] += weight
                heapq.heappush(heap, (-priority[adjacent], adjacent))

    t, s = A[-1], A[-2]
    cut_of_phase = priority[t]

    for adjacent, weight in out_graph[t].items():
        if adjacent != s:
            if adjacent in out_graph[s]:
                weight += out_graph[s][adjacent]

            out_graph[s][adjacent] = weight
            out_graph[adjacent][s] = weight

        del out_graph[adjacent][t]

    del out_graph[t]

    return cut_of_phase, (t, s)


def reconstruct(phase_idx: int, contractions: List[Tuple[str, str]]) -> Set[str]:
    subgraph: Dict[str, Set[str]] = {}
    for i in range(phase_idx):
        (t, s) = contractions[i]
        if t not in subgraph:
            subgraph[t] = set()
        if s not in subgraph:
            subgraph[s] = set()

        subgraph[t].add(s)
        subgraph[s].add(t)

    vertex = contractions[phase_idx][0]

    queue: List[str] = [vertex]
    partition: Set[str] = set(queue)
    while len(queue) != 0:
        vertex = queue.pop(0)
        for adjacent in subgraph[vertex]:
            if adjacent not in partition:
                queue.append(adjacent)
                partition.add(adjacent)

    return partition


if __name__ == "__main__":
    exit(main())
