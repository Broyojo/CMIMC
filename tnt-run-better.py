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
    return 0 <= i <= size - 1 and 0 <= j <= size - 1


def is_same_as_self(i, j):
    return my_i == i and my_j == j


def is_same_as_player(i, j):
    for player in players:
        if i == player["i"] and j == player["j"]:
            return True
    return False


def is_valid_tile(i, j):
    if in_grid(i, j):
        if arena[i][j] == 1:
            if not is_same_as_self(i, j):
                if not is_same_as_player(i, j):
                    return True
    return False


def count_valid_neighbors(i, j, exclude=[]):
    count = 0
    for di in range(-move_dist, move_dist + 1):
        for dj in range(-move_dist, move_dist + 1):
            new_i = i + di
            new_j = j + dj

            if new_i != i and new_j != j:
                if (new_i, new_j) not in exclude:
                    if is_valid_tile(new_i, new_j):
                        count += 1
    return count


def total_expected_reward(i, j, layers, memory={}, future_move_history=[]):
    # log(i, j)
    if layers == 0:
        return 0

    if (i, j) in memory:
        return memory[(i, j)]

    future_move_history.append((i, j))

    total_reward = 0

    for di in range(-move_dist, move_dist + 1):
        for dj in range(-move_dist, move_dist + 1):
            new_i = i + di
            new_j = j + dj

            valid_counts = count_valid_neighbors(
                new_i, new_j, exclude=future_move_history
            )

            total_reward += valid_counts + total_expected_reward(
                new_i, new_j, layers - 1, memory, future_move_history
            )

    memory[(i, j)] = total_reward
    return total_reward


def get_move(num_layers):
    moves = []
    for di in range(-move_dist, move_dist + 1):
        for dj in range(-move_dist, move_dist + 1):
            new_i = my_i + di
            new_j = my_j + dj
            if is_valid_tile(new_i, new_j):
                moves.append(
                    (
                        new_i,
                        new_j,
                        total_expected_reward(new_i, new_j, layers=num_layers),
                    )
                )

    if grace_moves_left > 0:
        new_i = my_i - 2
        new_j = my_j + 2
        for move in moves:
            if move[0] == new_i and move[1] == new_j:
                return (new_i, new_j)

    if len(moves) == 0:
        return (my_i, my_j)

    best_move = (0, 0, -1000)

    for move in moves:
        if move[2] > best_move[2]:
            best_move = move
    return move


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
    move = get_move(num_layers=5)

    output(move[0], move[1])
