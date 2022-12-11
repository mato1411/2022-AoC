import operator
import pathlib
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from typing import List

import numpy as np
from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


def get_monkey_details(monkey):
    if monkey.startswith("Monkey"):
        return int(monkey.split(":")[0].replace("Monkey", "").strip())
    if monkey.startswith("Starting"):
        return list(map(int, monkey.split(":")[1].strip().split(",")))
    if monkey.startswith("Operation"):
        tmp_op = monkey.split("=")[1].strip().split()
        op = [None, 0, None]
        for i in [0, 2]:
            try:
                op[i] = int(tmp_op[i])
            except Exception as e:
                continue
        match tmp_op[1]:
            case "+":
                op[1] = operator.add
            case "*":
                op[1] = operator.mul
        return op
    if monkey.startswith("Test"):
        return int(monkey.split("by")[1].strip())
    if monkey.startswith("If true"):
        return int(monkey.split("monkey")[1].strip())
    if monkey.startswith("If false"):
        return int(monkey.split("monkey")[1].strip())


@dataclass
class Monkey:
    no: int
    items: List
    op: List
    test: int
    true: int
    false: int
    count: int


def compute_monkey(monkeys, modulo):
    for m in monkeys:
        for i in m.items:
            m.count += 1
            values = []
            lvl = i
            for j in [0, 2]:
                if m.op[j] is None:
                    values.append(lvl)
                else:
                    values.append(m.op[j])
            lvl = m.op[1](values[0], values[1])
            if modulo:
                lvl %= modulo
            else:
                lvl //= 3
            if 0 == lvl % m.test:
                throw_to_m = m.true
            else:
                throw_to_m = m.false
            monkeys[throw_to_m].items.append(lvl)
        m.items = []


files = ["example.txt", input_file]

for f in files:
    list_input = [
        list(map(lambda x: get_monkey_details(x.strip()), m.split("\n")))
        for m in read_input(f, sep="\n\n")
    ]
    no = 0
    items = 1
    op = 2
    test = 3
    true = 4
    false = 5
    for part, max_rounds in zip(["Part 2"], [10000]):
        print(part, max_rounds)
        monkeys = []
        for m in list_input:
            monkeys.append(
                Monkey(
                    no=m[no],
                    items=m[items],
                    op=m[op],
                    test=m[test],
                    true=m[true],
                    false=m[false],
                    count=0,
                )
            )
        # mod = All test divisors multiplied
        mod = reduce(operator.mul, [m.test for m in monkeys])
        for round in range(max_rounds):
            if debug:
                print(f"Round {round + 1}")
            if debug:
                for m in monkeys:
                    print(f"Monkey: {m}")
            compute_monkey(monkeys, modulo=None if "1" in part else mod)
            if debug:
                for m in monkeys:
                    print(f"Monkey {m.no}: {m.count}")
        counts = []
        for m in monkeys:
            print(f"Monkey {m.no}: {m.count}")
            counts.append(m.count)
        print(f"{f} - {part}: {np.prod(np.array(sorted(counts)[-2:]))}")
