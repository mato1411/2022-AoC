import pathlib
from datetime import datetime

from utils import (
    down,
    down_left,
    down_right,
    get_input,
    left,
    read_input,
    right,
    up,
    up_left,
    up_right,
)

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


def get_adjacent_data(t):
    t_x, t_y = t
    adjacent_data = set()
    for d in [up, down, right, left, up_left, up_right, down_left, down_right]:
        adjacent_data.add((t_x + d[0], t_y + d[1]))
    return adjacent_data


def move(head, tail, x_move, y_move):
    head = (
        head[0] + x_move,
        head[1] + y_move,
    )
    tail_neighbours = get_adjacent_data(tail)
    if tail == head or head in tail_neighbours:
        return head, tail
    head_neighbours = get_adjacent_data(head)
    adjacent_spots = head_neighbours.intersection(tail_neighbours)
    move_diagonal = False
    if head[0] != tail[0] and head[1] != tail[1]:
        move_diagonal = True
    for spot in adjacent_spots:
        if len(adjacent_spots) == 1:
            return head, spot
        if spot == (tail[0] + x_move, tail[1] + y_move) and not move_diagonal:
            return head, spot
        if move_diagonal:
            for d in [up_left, up_right, down_left, down_right]:
                if spot == (tail[0] + d[0], tail[1] + d[1]):
                    return head, spot


files = ["example.txt", input_file]

for f in files:
    start = (0, 0)
    tail, head = start, start
    list_input = [i.split() for i in read_input(f)]
    directions = {"U": down, "D": up, "L": left, "R": right}
    tail_pos_visited = {start}
    for i, instruction in enumerate(list_input):
        x_move = directions[instruction[0]][0]
        y_move = directions[instruction[0]][1]
        for m in range(int(instruction[1])):
            new_head, new_tail = move(head, tail, x_move, y_move)
            head, tail = new_head, new_tail
            tail_pos_visited.add(tail)
    print(f"{f} - Part 1: {len(tail_pos_visited)}")
    print(f"{f} - Part 2: {0}")
