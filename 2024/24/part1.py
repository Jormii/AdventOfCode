import os
import re
import sys
import time
from enum import IntEnum
from typing import Dict, List
from collections import deque
from dataclasses import dataclass

BIGBOY = False

if not BIGBOY:
    SOLUTION = 69201640933606
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


class GateType(IntEnum):
    AND = 0
    OR = 1
    XOR = 2


@dataclass(slots=True, frozen=True)
class Gate:
    output: str
    type: GateType


@dataclass(slots=True, frozen=True)
class Input:
    ipt_1: str
    ipt_2: str


def main() -> int:
    t = time.perf_counter()

    _w_ = r'[a-z0-9]{3}'
    WIRE_PATTERN = re.compile(rf'^({_w_}): (\d)$')
    GATE_PATTERN = re.compile(rf'^({_w_}) (AND|OR|XOR) ({_w_}) -> ({_w_})$')

    wires: Dict[str, bool] = {}
    queue: deque[Input] = deque()
    gates: Dict[Input, List[Gate]] = {}
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

        it = iter(lines)
        for line in map(lambda ln: ln.strip(), it):
            if len(line) == 0:
                break

            assert (search := WIRE_PATTERN.search(line)) is not None

            wire = search.group(1)
            value = search.group(2) == '1'

            wires[wire] = value

        for line in map(lambda ln: ln.strip(), it):
            assert (search := GATE_PATTERN.search(line)) is not None

            input = Input(search.group(1), search.group(3))
            gate = Gate(search.group(4), GateType[search.group(2)])

            queue.append(input)
            if input not in gates:
                gates[input] = [gate]
            else:
                gates[input].append(gate)

    while len(queue) != 0:
        input = queue.popleft()
        if input.ipt_1 not in wires or input.ipt_2 not in wires:
            queue.append(input)
            continue

        input_1 = wires[input.ipt_1]
        input_2 = wires[input.ipt_2]

        for gate in gates[input]:
            match gate.type:
                case GateType.AND:
                    output = input_1 & input_2
                case GateType.OR:
                    output = input_1 | input_2
                case GateType.XOR:
                    output = input_1 ^ input_2
                case _:
                    raise NotImplementedError(gate.type)

            wires[gate.output] = output

    binary = 0
    for wire, value in wires.items():
        if value and wire[0] == 'z':
            binary |= 1 << int(wire[1:])

    tf = time.perf_counter()

    success = binary == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {binary} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
