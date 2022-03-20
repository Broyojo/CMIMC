from math import sqrt
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


def in_grid(i, j):
    return 0 <= i <= size-1 and 0 <= j <= size-1


def is_same_as_self(i, j):
    return my_i == i and my_j == j


def is_same_as_player(i, j):
    for player_index in range(len(players)):
        if players[player_index]["i"] == i and players[player_index]["j"] == j:
            return True
    return False


def is_near_player(i, j, distance):
    for di in range(-distance, distance + 1):
        for dj in range(-distance, distance + 1):
            new_i = i + di
            new_j = j + dj
            if is_same_as_player(new_i, new_j):
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
    for di in range(-move_dist, move_dist+1):
        for dj in range(-move_dist, move_dist+1):
            new_i = i + di
            new_j = j + dj

            if new_i != i and new_j != j and not (new_i, new_j) in memory:
                if is_valid_tile(new_i, new_j):
                    count += 1
    return count


def total_safe_layers(i, j, layers, initial_layers, path=[], memory=[]):
    layer = (initial_layers - layers, i, j)
    if layers == 0:
        return layer
    for coord in memory:
        if coord[1] == i and coord[2] == j:
            return coord
    di_list = (1, 0, -1, 2, -2)
    dj_list = (-1, 0, 1, -2, 2)
    for di in di_list:
        for dj in dj_list:
            new_i = i + di
            new_j = j + dj
            if is_valid_tile(new_i, new_j):
                if count_valid_neighbors(new_i, new_j, path) > 0 and (new_i, new_j) not in path and not is_near_player(new_i, new_j, 1):
                    # print("Checking layer", layer, new_i,
                    #     new_j, "and excluding:", memory, file=sys.stderr)
                    path_copy = [i for i in path]
                    path_copy.append((new_i, new_j))
                    temp_layer = total_safe_layers(
                        new_i, new_j, layers - 1, initial_layers, path_copy, memory)
                    memory.append(temp_layer)
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
    di_list = (1, 0, -1, 2, -2)
    dj_list = (-1, 0, 1, -2, 2)
    for di in di_list:
        for dj in dj_list:
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
        if count_valid_neighbors(move[2][1], move[2][2]) - 0.2 * distance_to_com((move[0], move[1])) > count_valid_neighbors(best_move[2][1], best_move[2][2]) - 0.2 * distance_to_com((best_move[0], best_move[1])):
            best_move = move
    return best_move

    # better_moves = []
    # for move in moves:
    #     if count_valid_neighbors(move[0], move[1]) > 0:
    #         better_moves.append(move)

    # if len(better_moves) != 0:
    #     return random.choice(better_moves)
    # else:
    #     return random.choice(moves)


def distance_to_com(pos):
    global center_of_mass
    return sqrt((center_of_mass[0] - pos[0])**2 + (center_of_mass[1] - pos[1])**2)

def output(i, j):
    print(json.dumps({"i": i, "j": j}))

center_of_mass = [12.5,12.5]
num_green = 25**2

def update_center_of_mass(players):
    global center_of_mass, num_green
    mass_sum = [center_of_mass[0] * num_green, center_of_mass[1] * num_green]
    for player in players:
        mass_sum[0] -= player["i"]
        mass_sum[1] -= player["j"]
        num_green -= 1
    center_of_mass = [mass_sum[0] / num_green, mass_sum[1] / num_green]

while True:
    _data = json.loads(input())
    arena = _data["arena"]

    players = _data["players"]
    my_index = _data["my_index"]
    grace_moves_left = _data["grace_moves_left"]

    me = players[my_index]
    my_i, my_j = me["i"], me["j"]

    my_history.append((my_i, my_j))

    # print(numpy.array(arena), file=sys.stderr)
    # print(my_i, my_j, file=sys.stderr)
    # print(total_safe_layers(my_i, my_j, 3, 3), file=sys.stderr)

    update_center_of_mass(players)

    move = get_move(num_layers=10)
    #print(move, file=sys.stderr)
    output(move[0], move[1])
