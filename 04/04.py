import pathlib
from datetime import datetime

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)

files = ["example.txt", input_file]

for f in files:
    list_input = read_input(f)
    sections = [
        list(map(lambda x: tuple(map(int, x.split("-"))), elves.split(",")))
        for elves in list_input
    ]
    sections_sets = []
    p1, p2 = 0, 0
    for tuples in sections:
        elve = []
        previous_t_to_set = None
        for t in tuples:
            t_to_set = set(range(t[0], t[1] + 1))
            if previous_t_to_set is None:
                previous_t_to_set = t_to_set
            else:
                if len(t_to_set.intersection(previous_t_to_set)) == len(
                    t_to_set
                ) or len(previous_t_to_set.intersection(t_to_set)) == len(
                    previous_t_to_set
                ):
                    p1 += 1
                    p2 += 1
                    continue
                if (
                    len(t_to_set.intersection(previous_t_to_set)) > 0
                    or len(previous_t_to_set.intersection(t_to_set)) > 0
                ):
                    p2 += 1
            elve.append(t_to_set)
        sections_sets.append(elve)
    print(f"{f} - Part 1: {p1}")
    print(f"{f} - Part 2: {p2}")
