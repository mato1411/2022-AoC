from datetime import datetime

from utils import get_input, read_input

debug = False
files = ["example.txt", "input.txt"]

for f in files:
    # str_input = get_input(year=2022, day=datetime.utcnow().day)
    max_calories_carried = 0
    top_3_calories_carried = []
    for i, elve in enumerate(
        [elves.split("\n") for elves in read_input(f, sep="\n\n")]
    ):
        calories_carried = sum(map(int, elve))
        if i < 3:
            top_3_calories_carried.append(calories_carried)
            continue
        if calories_carried > min(top_3_calories_carried):
            top_3_calories_carried.remove(min(top_3_calories_carried))
            top_3_calories_carried.append(calories_carried)
    print(f"{f} - Part 1: {max(top_3_calories_carried)}")
    print(f"{f} - Part 2: {sum(top_3_calories_carried)}")
