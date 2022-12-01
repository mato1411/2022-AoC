from datetime import datetime

from utils import read_input, get_input

debug = False
files = ['example.txt', 'input.txt']

for f in files:
    str_input = get_input(year=2022, day=datetime.utcnow().day)
    list_input = read_input(f, sep="\n\n")
    print(list_input)
    result = 0
    print(f"{f} - Part 1: {result}")
    print(f"{f} - Part 2: {result}")
