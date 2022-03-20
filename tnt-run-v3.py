import sys
import json
import random


def log(*args):
    print(*args, file=sys.stderr)


arena = []
my_i = 0
my_j = 0
players = []
grace_moves_left = 0
my_history = []
size = 25
move_dist = 2


def in_grid(i, j):
    return 0 <= i <= size-1 and 0 <= j <= size-1


def is_same_as_self(i, j):
    return my_i == i and my_j == j


def is_same_as_player(i, j):
    for p in range(len(players)):
        if i == players[p]["i"] and j == players[p]["j"]:
            return True
    return False


def is_valid_tile(i, j):
    if in_grid(i, j):
        if arena[i][j] == 1:
            if not is_same_as_self(i, j):
                if not is_same_as_player(i, j):
                    return True
    return False


def count_valid_neighbors(i, j):
    count = 0
    for di in range(-move_dist, move_dist+1):
        for dj in range(-move_dist, move_dist+1):
            new_i = my_i + di
            new_j = my_j + dj

            if is_valid_tile(new_i, new_j):
                count += 1
    return count


def generate_paths(num_paths=5):
    paths = {}

    current_node = (my_i, my_j)

    while count_valid_neighbors(paths) > 0:


def output(i, j):
    print(json.dumps({"i": i, "j": j}))


while True:
    _data = json.loads(input())
    arena = _data["arena"]
    players = _data["players"]
    my_index = _data["my_index"]
    grace_moves_left = _data["grace_moves_left"]

    me = players[my_index]
    my_i, my_j = me["i"], me["j"]
    my_history.append((my_i, my_j))

    move = get_move()

    output(move[0], move[1])
