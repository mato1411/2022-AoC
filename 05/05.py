import pathlib
import queue
import re
from datetime import datetime

from utils import get_2d_arr, get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)

files = ["example.txt", input_file]

for f in files:
    list_input = read_input(f, strip=False, sep="\n\n")
    stacks = list_input[0].split("\n")
    number_of_stacks = int(stacks[-1].split()[-1].strip())
    queues_p1 = [queue.LifoQueue() for n in range(number_of_stacks)]
    queues_p2 = [queue.LifoQueue() for n in range(number_of_stacks)]
    rows = []
    for stack in stacks[::-1][1:]:
        cols = []
        for q, j in enumerate(range(1, number_of_stacks * 4, 4)):
            try:
                value = stack[j].strip()
                if value:
                    queues_p1[q].put(value)
                    queues_p2[q].put(value)
            except IndexError as e:
                value = ""
            cols.append(value)
        rows.append(cols)
    print("Input:\n", get_2d_arr(rows[::-1], str))
    instructions = [
        list(map(int, re.findall(r"\d+", i))) for i in list_input[1].split("\n")
    ]
    for i in instructions[:-1]:
        removed_items, removed_items_p2 = [], []
        for j in range(i[0]):
            removed_items.append(queues_p1[i[1] - 1].get())
            removed_items_p2.append(queues_p2[i[1] - 1].get())
        for j1, j2 in zip(removed_items, removed_items_p2[::-1]):
            queues_p1[i[2] - 1].put(j1)
            queues_p2[i[2] - 1].put(j2)
    p1 = "".join([q.get() for q in queues_p1])
    p2 = "".join([q.get() for q in queues_p2])
    print(f"{f} - Part 1: {p1}")
    print(f"{f} - Part 2: {p2}")
