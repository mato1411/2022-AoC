import copy
import pathlib
from datetime import datetime

import numpy as np
from utils import get_2d_arr, get_directions_possible_of_xy, get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


def verify_tree(visible_trees, a, node):
    x, y = node
    current_height = a[x][y]
    # print(f"current_node: {node}")
    # print(f"current_height: {current_height}")
    x_max = a.shape[0]
    y_max = a.shape[1]
    dirs = get_directions_possible_of_xy(x, y, x_max, y_max, diag=False)
    for d in dirs:
        neighbour_height = a[x + d[0]][y + d[1]]
        neighbour_node = (x + d[0], y + d[1])
        match = False
        while True:
            if current_height > neighbour_height:
                # print(
                #    f"neighbour_node {neighbour_node}, neighbour_height is shorter: {neighbour_height}"
                # )
                n_x, n_y = neighbour_node
                # Is neighbour on the forest boarder?
                if n_x in (0, a.shape[0] - 1) or n_y in (
                    0,
                    a.shape[1] - 1,
                ):
                    # print(
                    #    f"Neighbor {neighbour_node} is on the edge, adding node: {node}"
                    # )
                    visible_trees.add(node)
                    match = True
                    break
                n_x, n_y = neighbour_node
                neighbour_node = (n_x + d[0], n_y + d[1])
                neighbour_height = a[n_x + d[0]][n_y + d[1]]
            else:
                break
        if match:
            break


def get_senic_score(node, a):
    x, y = node
    current_height = a[x][y]
    # print(f"current_node: {node}")
    # print(f"current_height: {current_height}")
    x_max = a.shape[0]
    y_max = a.shape[1]
    dirs = get_directions_possible_of_xy(x, y, x_max, y_max, diag=False)
    scores = []
    for d in dirs:
        score = 1
        neighbour_height = a[x + d[0]][y + d[1]]
        neighbour_node = (x + d[0], y + d[1])
        while True:
            if current_height <= neighbour_height:
                # print(
                #    f"neighbour_node {neighbour_node}, neighbour_height is higher: {neighbour_height}"
                # )
                break
            n_x, n_y = neighbour_node
            if n_x in (0, a.shape[0] - 1) or n_y in (
                0,
                a.shape[1] - 1,
            ):
                break
            score += 1
            neighbour_node = (n_x + d[0], n_y + d[1])
            neighbour_height = a[n_x + d[0]][n_y + d[1]]
        scores.append(score)
    # print(scores)
    return np.prod(np.array(scores))


files = ["example.txt", input_file]

for f in files:
    list_input = read_input(f)
    forest = get_2d_arr(list_input, int)
    print(forest)
    outer_trees = set()
    for x in range(forest.shape[0]):
        outer_trees.add((x, 0))
        outer_trees.add((x, forest.shape[1] - 1))
    for y in range(forest.shape[1]):
        outer_trees.add((0, y))
        outer_trees.add((forest.shape[0] - 1, y))
    visible_trees = copy.deepcopy(outer_trees)
    inner_forest = forest[1:-1, 1:-1]
    for x in range(inner_forest.shape[0]):
        for y in range(inner_forest.shape[1]):
            assert inner_forest[x][y] == forest[x + 1][y + 1]
            verify_tree(visible_trees, forest, (x + 1, y + 1))
    print(f"{f} - Part 1: {len(visible_trees)}")
    scenic_scores = []
    for tree in visible_trees.difference(outer_trees):
        scenic_scores.append(get_senic_score(tree, forest))
    print(f"{f} - Part 2: {max(scenic_scores)}")
