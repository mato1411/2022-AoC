import pathlib
from datetime import datetime

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)

files = ["example.txt", input_file]
mapping_to_numbers = dict(A=1, B=2, C=3, X=1, Y=2, Z=3)
lost = 0
draw = 3
won = 6
mapping_to_result = dict(X=lost, Y=draw, Z=won)

# Rock 1 defeats Scissors 3, Scissors 3 defeats Paper 2, and Paper 2 defeats Rock 1.
# 1 > 3, 3 > 2, 2 > 1
# 1 == 1
# 1 < 2
# 1 > 3
# 2 > 1
# 2 == 2
# 2 < 3
# 3 < 1
# 3 > 2
# 3 == 3


def get_result(a, b):
    if a == b:
        return a + draw
    if (a == 1 and b == 3) or (a == 2 and b == 1) or (a == 3 and b == 2):
        return a + won
    return a


def get_a(b, result):
    if result == draw:
        return b
    if result == won:
        if b == 3:
            return 1
        if b == 2:
            return 3
        if b == 1:
            return 2
    if b == 3:
        return 2
    if b == 2:
        return 1
    if b == 1:
        return 3


for f in files:
    p1 = []
    p2 = []
    list_input = [game.split() for game in read_input(f)]
    for game in list_input:
        opponent_choice = mapping_to_numbers[game[0]]
        my_choice = mapping_to_numbers[game[1]]
        result_expected = mapping_to_result[game[1]]
        p1.append(get_result(my_choice, opponent_choice))
        p2.append(get_a(opponent_choice, result_expected) + result_expected)
    print(f"{f} - Part 1: {sum(p1)}")
    print(f"{f} - Part 2: {sum(p2)}")
