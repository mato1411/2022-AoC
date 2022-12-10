import pathlib
from datetime import datetime
from typing import Dict

import numpy as np
from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


def check_cycle(results: Dict[int, int], cycle: int, x: int):
    if cycle in [20, 60, 100, 140, 180, 220]:
        results[cycle] = cycle * x


def draw_pixel_in_crt(crt, cycle: int, x: int):
    row = (cycle - 1) // crt.shape[1]
    col = (cycle - 1) % crt.shape[1]
    sprite = [x - 1, x, x + 1]

    if col in sprite:
        crt[row][col] = "#"
    if debug:
        print("------------")
        print(f"cycle {cycle}")
        print(f"x: {x}")
        print(f"cursor: {col}")
        print(f"row: {row}")
        print(f"sprite: {sprite}")
        print(f"CRT: {''.join(list(crt[row, :]))}")


files = ["example2.txt", input_file]

for f in files:
    list_input = read_input(f)
    if debug:
        print(list_input)
    x = 1
    cycle = 1
    crt = np.full(shape=(6, 40), fill_value=".", dtype=str)
    p1 = dict()
    for command in list_input:
        commands = command.split()
        if debug:
            print(commands)
        is_noop = False
        if len(commands) > 1:
            op = commands[0]
            n = int(commands[1])
        else:
            is_noop = True
        if cycle == 15:
            # exit(1)
            pass
        check_cycle(p1, cycle, x)

        if is_noop:
            draw_pixel_in_crt(crt, cycle, x)
            cycle += 1
        else:
            for i in range(2):
                draw_pixel_in_crt(crt, cycle, x)
                cycle += 1
                check_cycle(p1, cycle, x)
            x = x + n

    print(f"{f} - Part 1: {sum(p1.values())}")
    print(f"{f} - Part2 CRT:")
    for x in range(crt.shape[0]):
        print("".join(list(crt[x, :])))
    result = 0
