import sys
import json
import random

arena = []
my_i = 0
my_j = 0
players = []
grace_moves_left = 0
my_history = []
size = 25
move_dist = 2
count = 0


def in_grid(i, j):
    return 0 <= i <= size-1 and 0 <= j <= size-1


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


def count_valid_neighbors(i, j, memory=[]):
    count = 0
    for di in random.shuffle(range(-move_dist, move_dist+1)):
        for dj in random.shuffle(range(-move_dist, move_dist+1)):
            new_i = i + di
            new_j = j + dj

            if new_i != i and new_j != j and not (new_i, new_j) in memory:
                if is_valid_tile(new_i, new_j):
                    count += 1
    return count


def total_safe_layers(i, j, layers, initial_layers, memory=[]):
    layer = (initial_layers - layers, i, j)
    if layers == 0:
        return layer
    for di in range(-move_dist, move_dist+1):
        for dj in range(-move_dist, move_dist+1):
            new_i = i + di
            new_j = j + dj
            if is_valid_tile(new_i, new_j):
                if count_valid_neighbors(new_i, new_j) > 0 and (new_i, new_j) not in memory:
                    # print("Checking layer", layer, new_i,
                    #     new_j, "and excluding:", memory, file=sys.stderr)
                    memory_copy = [i for i in memory]
                    memory_copy.append((new_i, new_j))
                    temp_layer = total_safe_layers(
                        new_i, new_j, layers - 1, initial_layers, memory_copy)
                    if temp_layer[0] > layer[0]:
                        layer = temp_layer
                    # print("Layer", layer, "out of",
                    #      initial_layers, file=sys.stderr)
                    if layer[0] == initial_layers:
                        return layer

    return layer


def get_move(num_layers):
    if grace_moves_left > 0:
        new_i = my_i - 2
        new_j = my_j + 2
        return (new_i, new_j)

    moves = []
    for di in range(-move_dist, move_dist+1):
        for dj in range(-move_dist, move_dist+1):
            new_i = my_i + di
            new_j = my_j + dj
            if is_valid_tile(new_i, new_j):
                moves.append(
                    (new_i, new_j, total_safe_layers(new_i, new_j, layers=num_layers, initial_layers=num_layers)))

    if len(moves) == 0:
        return (my_i, my_j)
    best_moves = []
    for layers in range(num_layers, -1, -1):
        for move in moves:
            if move[2][0] == layers:
                best_moves.append(move)
    #print(best_move, file=sys.stderr)
    best_move = best_moves[0]
    for move in best_moves:
        if count_valid_neighbors(move[2][1], move[2][2]) > count_valid_neighbors(best_move[2][1], best_move[2][2]):
            best_move = move
    return random.choice(best_moves)

    # better_moves = []
    # for move in moves:
    #     if count_valid_neighbors(move[0], move[1]) > 0:
    #         better_moves.append(move)

    # if len(better_moves) != 0:
    #     return random.choice(better_moves)
    # else:
    #     return random.choice(moves)


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

    if count <= 2:
        # print(numpy.array(arena), file=sys.stderr)
        # print(my_i, my_j, file=sys.stderr)
        # print(total_safe_layers(my_i, my_j, 3, 3), file=sys.stderr)
        count += 1

    move = get_move(num_layers=8)
    #print(move, file=sys.stderr)
    output(move[0], move[1])
