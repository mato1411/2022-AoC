import pathlib
from dataclasses import dataclass
from datetime import datetime
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
        return monkey.split("=")[1].strip().replace("old", "{}")
    if monkey.startswith("Test"):
        return "{} % " + monkey.split("by")[1].strip()
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
    op: str
    test: str
    true: int
    false: int
    count: int


def compute_monkey(monkeys, modulo_3=True):
    for m in monkeys:
        if debug:
            print(m)
        for i in m.items:
            m.count += 1
            lvl = eval(
                m.op.format(i, i)
                if m.op.find("{") != len(m.op) - m.op.rfind("{")
                else m.op.format(i)
            )
            if modulo_3:
                lvl //= 3
            if 0 == eval(m.test.format(lvl)):
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
    for part, max_rounds in zip(["Part 1"], [20]):
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
        for round in range(max_rounds):
            if debug:
                print(f"Round {round + 1}")
            compute_monkey(monkeys)
            if debug:
                for m in monkeys:
                    print(f"Monkey {m.no}: {m.items}")
        counts = []
        for m in monkeys:
            print(f"Monkey {m.no}: {m.count}")
            counts.append(m.count)
        print(f"{f} - {part}: {np.prod(np.array(sorted(counts)[-2:]))}")
