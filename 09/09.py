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


def move(head, tail, x_move, y_move, move_head=True):
    if move_head:
        head = (
            head[0] + x_move,
            head[1] + y_move,
        )
    tail_neighbours = get_adjacent_data(tail)

    if tail == head or head in tail_neighbours:
        return head, tail

    if tail[0] == head[0]:
        if tail[1] < head[1]:
            return head, (tail[0], tail[1] + 1)
        else:
            return head, (tail[0], tail[1] - 1)

    if tail[1] == head[1]:
        if tail[0] < head[0]:
            return head, (tail[0] + 1, tail[1])
        else:
            return head, (tail[0] - 1, tail[1])

    if tail[0] < head[0]:
        tail = (tail[0] + 1, tail[1])
    else:
        tail = (tail[0] - 1, tail[1])

    if tail[1] < head[1]:
        tail = (tail[0], tail[1] + 1)
    else:
        tail = (tail[0], tail[1] - 1)

    return head, tail


files = ["example.txt", "example2.txt", input_file]

for f in files:

    start = (0, 0)
    list_input = [i.split() for i in read_input(f)]
    directions = {"U": down, "D": up, "L": left, "R": right}

    tail_p1_visited = {start}
    tail_p2_visited = {start}

    p1_knots = [start] * 2
    p2_knots = [start] * 10

    for i, instruction in enumerate(list_input):
        x_move = directions[instruction[0]][0]
        y_move = directions[instruction[0]][1]
        for m in range(int(instruction[1])):
            p1_knots[0], p1_knots[1] = move(
                p1_knots[0], p1_knots[1], x_move, y_move, move_head=True
            )
            tail_p1_visited.add(p1_knots[-1])
            new_head, new_follower = move(
                p2_knots[0], p2_knots[1], x_move, y_move, move_head=True
            )
            p2_knots[0], p2_knots[1] = new_head, new_follower
            for j in range(1, len(p2_knots) - 1):
                follower_1, follower_2 = move(
                    p2_knots[j], p2_knots[j + 1], x_move, y_move, move_head=False
                )
                p2_knots[j], p2_knots[j + 1] = follower_1, follower_2
                tail_p2_visited.add(p2_knots[-1])
    print(f"{f} - Part 1: {len(tail_p1_visited)}")
    print(f"{f} - Part 2: {len(tail_p2_visited)}")
