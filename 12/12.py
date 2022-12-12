import pathlib
from datetime import datetime
from heapq import heappop, heappush

from utils import get_adjacent_data, get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


def a_star_no_heuristic(a, start, end):
    not_visited = [(0, a[start[0]][start[0]], start)]
    parents = {start: 0}
    while not_visited:
        step, height, node = heappop(not_visited)
        if node in end:
            return parents[node], step
        for neighbor, n_height in get_adjacent_data(a, node).items():
            new_height = parents[node] + 1
            if n_height <= height + 1:
                if neighbor not in parents or parents[neighbor] > new_height:
                    parents[neighbor] = new_height
                    heappush(not_visited, (new_height, n_height, neighbor))


files = [input_file]

for f in files:
    list_input = read_input(f)
    a1 = [list(r) for r in list_input]
    a2 = [list(r) for r in list_input]
    end2 = []
    for r in range(len(list_input)):
        for c in range(len(list_input[0])):
            if list_input[r][c] == "S":
                start = (r, c)
            if list_input[r][c] == "E":
                end1 = [(r, c)]
            if list_input[r][c] == "a":
                end2.append((r, c))
            a1[r][c] = int(ord(list_input[r][c]))
            a2[r][c] = -1 * int(ord(list_input[r][c]))
    dist1 = a_star_no_heuristic(a1, start, end1)
    # For part 2 move backwards and invert the heights and
    # have multiple possible ends
    dist2 = a_star_no_heuristic(a2, *end1, end2)
    print(f"{f} - Part 1: {dist1}")
    print(f"{f} - Part 2: {dist2}")
