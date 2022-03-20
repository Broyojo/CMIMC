import sys
import json
import random

### Global Variables ###

DATA = json.loads(input())
GENERATOR = DATA["generator"]
ROLE = DATA["role"]
PARAMETER = DATA["parameter"]
AIRSPACE = DATA["airspace"] if ROLE == "tower" else []
BITS = DATA["role"] if ROLE == "drone" else []
BOARD_SIZE = 256
MAX_MSG_SIZE = 64

START_POS_BITS = 8
MOVEMENT_BITS = 5
TURN_BITS = 2

UP = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)

### Utility Functions ###


def tower_output(bits):
    print(json.dumps({"bits": bits}))


def drone_output(col, moves):
    print(json.dumps({"col": col, "moves": moves}))


def debug_print(*args):
    print(*args, file="file.txt")


def str_dir(dir):
    if dir == UP:
        return "UP"
    elif dir == LEFT:
        return "LEFT"
    elif dir == RIGHT:
        return "RIGHT"
    else:
        quit("unknown direction:", dir)


def is_valid(i, j):
    return 0 <= i <= BOARD_SIZE-1 and 0 <= j <= BOARD_SIZE-1 and AIRSPACE[i][j] == 0


def valid_starting_cols():
    columns = []
    for column_index in range(255):
        if AIRSPACE[255][column_index] == 0:
            columns.append(column_index)
    return columns


def upward_dist_to_obstacle(i, j):
    dist = 0
    while True:
        i -= 1
        if not is_valid(i, j):
            break
        dist += 1
    return dist


def create_path(i, j):
    path = []  # list of (dir, dict)
    while True:
        dist = upward_dist_to_obstacle(i, j)

        new_i, new_j = i - dist, j  # move up until you get to obstacle

        if new_i == 0:  # at the top of the board
            break

        path.append((UP, dist))

        dir_list = []
        if is_valid(new_i, new_j + LEFT[1]):
            dir_list.append(LEFT)
        if is_valid(new_i, new_j + RIGHT[1]):
            dir_list.append(RIGHT)

        if len(dir_list) == 0:  # the player is stuck
            break

        dir = random.choice(dir_list)

        new_j += dir[1]

        path.append((dir, 1))

        i, j = new_i, new_j

    return path
    ### Program Entry Point ###


def main():
    if ROLE == "tower":
        valid_cols = valid_starting_cols()
        path = create_path(BOARD_SIZE, valid_cols[0])
        debug_print(path)
    if ROLE == "drone":
        pass


main()
