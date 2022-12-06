import pathlib
from datetime import datetime

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)

files = ["example.txt", input_file]


def run(list_input: list[str], no_distinct_chars=4):
    for i in range(0, len(list_input), 1):
        start_of_pattern = list_input[i : i + no_distinct_chars]
        if len(set(start_of_pattern)) == no_distinct_chars:
            return i + no_distinct_chars


for f in files:
    for line in read_input(f):
        print(line)
        p1 = run(line)
        p2 = run(line, 14)
        print(f"{f} - Part 1: {p1}")
        print(f"{f} - Part 2: {p2}")
