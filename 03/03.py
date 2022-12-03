import pathlib
import string
from datetime import datetime

from utils import read_input, get_input

debug = False
input_file = 'input.txt'

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)

files = ['example.txt', input_file]
prio = list(string.ascii_lowercase) + list(string.ascii_uppercase)

for f in files:
    list_input = read_input(f)
    p1 = []
    rucksack_sets = [(set(rucksack[:len(rucksack)//2]), set(rucksack[len(rucksack)//2:])) for rucksack in list_input]
    for r_set in rucksack_sets:
        intersect_char = list(r_set[0].intersection(r_set[1]))[0]
        p1.append(prio.index(intersect_char) + 1)
    p2 = []
    next_end = 3
    for i in range(0, len(list_input), 3):
        next_end += i
        rucksack_badge = [set(rb) for rb in list_input[i:next_end]]
        intersect_char = list(rucksack_badge[0] & rucksack_badge[1] & rucksack_badge[2])[0]
        p2.append(prio.index(intersect_char) + 1)
    print(f"{f} - Part 1: {sum(p1)}")
    print(f"{f} - Part 2: {sum(p2)}")
