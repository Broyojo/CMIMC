import sys
import json
import random

# INPUT FORMAT (per turn):
'''
    "arena": A 2D (25 x 25) list of integers representing the current
        arena state, 1 for a present tile and 0 for empty.
        Can be indexed via arena[i][j].
    "players": For every player, a dict containing
        "alive": whether they are alive or dead.
        "i", "j": their zero-indexed coordinates.
        The order of the players remains consistent in this list.
    "my_index": Which index into the "players" list you are.
    "grace_moves_left": How many grace moves are remaining (if any),
        i.e. if this is 1, then on your next move, the ground currently
        underneath you does not disappear, but if this is 0 it does.
'''
# OUTPUT FORMAT (per turn):
'''
    "i", "j": Your destination coordinates. Each coordinate can differ by
        at most 2 from your previous coordinates.
'''
# Function for handling output


def output(i, j):
    print(json.dumps({"i": i, "j": j}))


def check_tile(arena, i, j, my_i, my_j):
    return i != my_i or j != my_j and i in range(25) and j in range(25) and arena[i][j] == 1


# def check_new_tile(arena, i, j, my_i, my_j):
#     valid_tiles = 0
#     for di in range(-2, 2):
#         for dj in range(-2, 2):
#             if check_tile(arena, new_i, new_j, my_i, my_j):
#                 valid_tiles += 1
#     return valid_tiles


def check_new_tile_rec(arena, i, j, layers, my_i, my_j):
    score = 0
    if layers > 0:
        valid_tiles = 0
        for di in range(-2, 3):
            for dj in range(-2, 3):
                new_i = i + di
                new_j = j + dj
                if check_tile(arena, new_i, new_j, my_i, my_j):
                    score += 0.5 * \
                        check_new_tile_rec(
                            arena, new_i, new_j, layers - 1, my_i, my_j)
                    valid_tiles += 1
        return score
    return 0


def get_move(arena, my_i, my_j, layers):
    moves = []
    for di in range(-2, 3):
        for dj in range(-2, 3):
            new_i = my_i + di
            new_j = my_j + dj
            if new_i in range(25) and new_j in range(25):
                if check_tile(arena, new_i, new_j, my_i, my_j):
                    moves.append(
                        (new_i, new_j, check_new_tile_rec(arena, new_i, new_j, 1, my_i, my_j)))

    max = (0, 0, -1000)
    print(len(moves), file=sys.stderr)
    for move in moves:
        if move[2] > max[2]:
            max = move
    if max in moves:
        return max
    if len(moves) > 0:
        return random.choice(moves)

    return (0, 0)


# You can store globals outside of the main loop
my_history = []
size = 25
print("example print", file=sys.stderr)

while True:
    # Fetches input from grader (no need to edit)
    _data = json.loads(input())
    arena = _data["arena"]
    players = _data["players"]
    my_index = _data["my_index"]
    grace_moves_left = _data["grace_moves_left"]
    # End input

    me = players[my_index]
    my_i, my_j = me["i"], me["j"]
    my_history.append((my_i, my_j))

    move = get_move(arena, my_i, my_j, 2)
    output(move[0], move[1])
