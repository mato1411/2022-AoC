import pathlib
from dataclasses import dataclass
from datetime import datetime

import numpy as np
from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Coordinate(x=self.x - other.x, y=self.y - other.y)


def add_char_to_a(a, coord, char="#", use_offset=True):
    x_offset = 0
    y_offset = 0 if a.shape[1] > 30 or not use_offset else 485
    a[coord.x - x_offset][coord.y - y_offset] = char


def rock_distance(arr, a, b):
    distance = a - b
    if distance.y != 0:
        if distance.y < 0 and distance.x == 0:
            r = range(a.y, b.y)
        elif distance.y > 0:
            r = range(b.y, a.y)
        for y in r:
            add_char_to_a(arr, Coordinate(x=a.x, y=y))
    if distance.x != 0 and distance.y == 0:
        if distance.x < 0:
            r = range(a.x, b.x)
        elif distance.x > 0:
            r = range(b.x, a.x)
        for x in r:
            add_char_to_a(arr, Coordinate(x=x, y=a.y))


def print_array(a):
    for x in range(a.shape[0]):
        print("".join(list(a[x, :])))


def move_until_rest(a, coord, shape, stop_at_floor):
    y_offset = 0 if a.shape[1] > 30 else 485
    x, y = coord.x, coord.y - y_offset
    while True:
        new_x = x + 1
        new_y = y
        if a[new_x][y] != ".":
            new_y = y + -1
            if stop_at_floor and new_y < 0:
                return False
            if a[new_x][new_y] != ".":
                new_y = y + 1
                if stop_at_floor and new_y > shape[1]:
                    return False
                if a[new_x][new_y] != ".":
                    if stop_at_floor and new_x == shape[0]:
                        return False
                    a[x][y] = "o"
                    if not stop_at_floor and x == 0 and y == 500 - y_offset:
                        return False
                    return True
        x = new_x
        y = new_y


files = ["example.txt", input_file]
shapes = [(20, 30), (200, 800)]

for f, s in zip(files, shapes):
    list_input = [
        list(
            map(
                lambda x: Coordinate(
                    x=int(x.strip().split(",")[1]), y=int(x.strip().split(",")[0])
                ),
                y.split("->"),
            )
        )
        for y in read_input(f)
    ]
    if debug:
        print(list_input)
    x_max = 0
    arr = np.full(shape=s, fill_value=".", dtype=str)
    for rock_info in list_input:
        for i in range(len(rock_info) - 1):
            a = rock_info[i]
            b = rock_info[i + 1]
            add_char_to_a(arr, a)
            add_char_to_a(arr, b)
            rock_distance(arr, a, b)
            if a.x > x_max:
                x_max = a.x
    sand_start = Coordinate(x=0, y=500)
    floor_x = x_max + 2
    for y in range(s[1]):
        add_char_to_a(arr, Coordinate(floor_x, y), use_offset=False)
    if debug:
        print_array(arr)
    total_sand_unit = 0
    for stop_at_floor in [True, False]:
        sand_units = 0 if stop_at_floor else 1
        add_char_to_a(arr, sand_start, char="+")
        try:
            while move_until_rest(arr, sand_start, (floor_x, s[1]), stop_at_floor):
                # print_array(arr)
                sand_units += 1
        except IndexError as e:
            print(e)
        if debug:
            print_array(arr)
        total_sand_unit += sand_units
        print(f"{f} - Part {1 if stop_at_floor else 2}: {total_sand_unit}")
