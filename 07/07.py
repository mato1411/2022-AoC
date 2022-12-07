import pathlib
from datetime import datetime
from pprint import pprint
from typing import Dict, Tuple

from utils import get_input, read_input

debug = False
input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2022, day=datetime.utcnow().day)


class FsDirNode:
    def __init__(self, name: str):
        self.dir = name
        self.files = []
        self.dirs = []
        self.previous_dir = None
        self.sum_file_size = 0
        self.total_size = 0

    def add_file(self, file: Tuple[int, str]):
        self.files.append(file)

    def add_dir(self, name: str):
        new_dir = FsDirNode(name=name)
        self.dirs.append(new_dir)
        new_dir.previous_dir = self
        return new_dir

    def get_previous_node(self):
        return self.previous_dir

    def compute_sizes(self):
        for d in self.dirs:
            d.compute_sizes()
        sum_file_size = sum([f[0] for f in self.files])
        self.sum_file_size = sum_file_size
        self.total_size += sum_file_size
        if self.previous_dir:
            prev = self.get_previous_node()
            prev.total_size += self.total_size

    def get_total_sizes(self, results: Dict[str, int], max_size=None, min_size=0):
        for d in self.dirs:
            d.get_total_sizes(results, max_size, min_size)

        if (max_size and self.total_size <= max_size) or (
            min_size and self.total_size >= min_size
        ):
            prev = self.get_previous_node()
            prefix = prev.dir if prev else ""
            results[f"{prefix}/{self.dir}"] = self.total_size


files = ["example.txt", input_file]
cd_start = "$ cd "
dir_start = "dir "
ls_start = "$ ls"

for f in files:
    list_input = read_input(f)
    # print(list_input)
    root = FsDirNode(name=list_input[0].replace(cd_start, "").strip())
    cwd = root
    for output in list_input[1:]:
        if output.startswith(cd_start):
            new_dir = output.replace(cd_start, "").strip()
            if new_dir == "..":
                cwd = cwd.get_previous_node()
            else:
                cwd = cwd.add_dir(name=new_dir)
            continue
        if output[0].isdigit():
            size_file = int(output.split()[0]), output.split()[1]
            cwd.add_file(size_file)

    root.compute_sizes()
    p1 = dict()
    root.get_total_sizes(max_size=100000, results=p1)
    unused_space = 70000000 - root.total_size
    required_unused_space = 30000000
    space_to_be_freed = required_unused_space - unused_space
    p2 = dict()
    root.get_total_sizes(min_size=space_to_be_freed, results=p2)
    print(f"{f} - Part 1: {sum(p1.values())}")
    print(f"{f} - Part 2: {sorted(list(p2.values()))[0]}")
