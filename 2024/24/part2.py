import os
import re
import sys
import time
from enum import IntEnum
from typing import Dict, List, Set
from dataclasses import dataclass

BIGBOY = False

if not BIGBOY:
    SOLUTION = 'dhq,hbs,jcp,kfp,pdg,z18,z22,z27'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = '-1'
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
    gates: Dict[str, List[Gate]] = {}
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

            for wire in (input.ipt_1, input.ipt_2):
                if wire not in gates:
                    gates[wire] = [gate]
                else:
                    gates[wire].append(gate)

    # NOTE: Needed help

    wrong: Set[str] = set()
    n_bits = len(wires) >> 1
    for wire in gates.keys():
        for gate in gates[wire]:
            # - AND -
            if gate.type == GateType.AND:
                if wire == 'x00' or wire == 'y00':
                    pass
                elif gate.output not in gates:
                    wrong.add(gate.output)
                else:
                    for other_gate in gates[gate.output]:
                        if other_gate.type != GateType.OR:
                            wrong.add(gate.output)

            # - OR -
            elif gate.type == GateType.OR:
                if gate.output == f'z{n_bits:02}':
                    pass
                elif gate.output not in gates:
                    wrong.add(gate.output)
                else:
                    for other_gate in gates[gate.output]:
                        if other_gate.type == GateType.OR:
                            wrong.add(gate.output)
            # - XOR -
            elif gate.type == GateType.XOR:
                if gate.output[0] == 'z':
                    pass
                elif (wire[0] != 'x' and wire[0] != 'y') and gate.output[0] != 'z':
                    wrong.add(gate.output)
                else:
                    for other_gate in gates[gate.output]:
                        if other_gate.type == GateType.OR:
                            wrong.add(gate.output)

    solution = ','.join(sorted(wrong))

    tf = time.perf_counter()

    success = solution == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {solution} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
