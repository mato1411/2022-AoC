import ast
import pathlib
from datetime import datetime
from functools import cmp_to_key

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


def parse_paket(x: str):
    x = ast.literal_eval(x)
    return x


def compare_ints(a, b):
    if a == b:
        return None
    return True if a < b else False


def compare_int_with_list(a, b, is_list="a"):
    if is_list == "a":
        return compare_list_with_list(a, [b])
    else:
        return compare_list_with_list([a], b)


def compare_list_with_list(la, lb):
    max_len = len(la) if len(la) > len(lb) else len(lb)
    if la == lb:
        return None
    for i in range(max_len):
        try:
            a = la[i]
        except IndexError:
            right_order = True
            break
        try:
            b = lb[i]
        except IndexError:
            right_order = False
            break
        if isinstance(a, int):
            if isinstance(b, int):
                right_order = compare_ints(a, b)
                if right_order is not None:
                    break
            if isinstance(b, list):
                right_order = compare_int_with_list(a, b, is_list="b")
                if right_order is not None:
                    break
        if isinstance(a, list):
            if isinstance(b, int):
                right_order = compare_int_with_list(a, b, is_list="a")
                if right_order is not None:
                    break
            if isinstance(b, list):
                right_order = compare_list_with_list(a, b)
                if right_order is not None:
                    break
    return right_order


def compare_list_with_list_cmp(la, lb):
    max_len = len(la) if len(la) > len(lb) else len(lb)
    if la == lb:
        return 0
    for i in range(max_len):
        try:
            a = la[i]
        except IndexError:
            right_order = True
            break
        try:
            b = lb[i]
        except IndexError:
            right_order = False
            break
        if isinstance(a, int):
            if isinstance(b, int):
                right_order = compare_ints(a, b)
                if right_order is not None:
                    break
            if isinstance(b, list):
                right_order = compare_int_with_list(a, b, is_list="b")
                if right_order is not None:
                    break
        if isinstance(a, list):
            if isinstance(b, int):
                right_order = compare_int_with_list(a, b, is_list="a")
                if right_order is not None:
                    break
            if isinstance(b, list):
                right_order = compare_list_with_list(a, b)
                if right_order is not None:
                    break
    return 1 if right_order else -1


files = ["example.txt", input_file]

for f in files:
    list_input = [x.split("\n") for x in read_input(f, sep="\n\n")]
    order_p1 = []
    order_p2 = []
    for x in list_input:
        if debug:
            print("-----start")
            print(x)
        la = parse_paket(x[0])
        lb = parse_paket(x[1])
        order_p2.append(la)
        order_p2.append(lb)
        right_order = compare_list_with_list(la, lb)
        order_p1.append(right_order)
    divider_pakets = [[[2]], [[6]]]
    for p in divider_pakets:
        order_p2.append(p)
    order_p2 = sorted(
        order_p2, key=cmp_to_key(compare_list_with_list_cmp), reverse=True
    )
    print(order_p2)
    print(f"{f} - Part 1: {sum([i+1 for i in range(len(order_p1)) if order_p1[i]])}")
    print(
        f"{f} - Part 2: {(order_p2.index(divider_pakets[0]) + 1) * (order_p2.index(divider_pakets[1]) + 1)}"
    )
