import random
import json
import heapq
from math import *
from sys import stderr

# INPUT FORMAT (initial, ONLY HAPPENS ONCE):
"""
    "layout": A 2D (64x64) list of 0, 1, or 2, describing the grid layout,
        where 0 is a floor, 1 is a wall, and 2 is the target destination.
        Can be indexed via layout[i][j].
"""
# INPUT FORMAT (per turn):
"""
    "view": A 2D (3x3) list of 0, 1, or 2, describing the area immediately
        around the robot, oriented in the direction the robot is facing.
        Can be indexed via view[i][j].
"""
# OUTPUT FORMAT (per turn):
"""
    "move": one of "forward", "backward", "left", "right", "apparate"
"""


def is_valid_location(pos):
    if pos[0] >= 0 and pos[1] >= 0 and pos[0] < 64 and pos[1] < 64:
        return layout[pos[0]][pos[1]] != 1
    return False


def neighbors(pos):
    return [
        (pos[0], pos[1] - 1),
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] + 1),
    ]


def compute_paths(goal):
    paths = {}
    frontier = [DijkstraNode(goal, None)]
    heapq.heapify(frontier)
    frontier_set = set(frontier)
    visited = set()

    while len(frontier) != 0:
        next_node = heapq.heappop(frontier)
        visited.add(next_node)
        frontier_set.remove(next_node)
        for neighbor in neighbors(next_node.pos):
            if not is_valid_location(neighbor):
                continue
            n = DijkstraNode(neighbor, next_node)
            if n in visited:
                continue
            if n not in frontier_set:
                frontier_set.add(n)
                heapq.heappush(frontier, n)
            else:
                for e in frontier_set:
                    if e == n:
                        if e > n:
                            e.set_parent(next_node)
                        break

    for node in visited:
        if node.parent != None:
            paths[str((node.pos[0], node.pos[1]))] = node.parent.pos
        else:
            paths[str((node.pos[0], node.pos[1]))] = None

    return paths


class DijkstraNode:
    pos = (0, 0)
    parent = None
    cost = 0

    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent
        if self.parent == None:
            self.cost = 0
        else:
            self.set_cost()

    def set_parent(self, new_parent):
        self.parent = new_parent
        self.set_cost()

    def set_cost(self):
        step_cost = sqrt(
            (self.pos[0] - self.parent.pos[0]) ** 2
            + (self.pos[1] - self.parent.pos[1]) ** 2
        )
        self.cost = self.parent.cost + step_cost

    def __eq__(self, other) -> bool:
        if type(other) == DijkstraNode:
            return self.pos == other.pos
        return False

    def __ne__(self, other) -> bool:
        if type(other) == DijkstraNode:
            return self.pos != other.pos
        return True

    def __lt__(self, other) -> bool:
        return self.cost < other.cost

    def __gt__(self, other) -> bool:
        return self.cost > other.cost

    def __le__(self, other) -> bool:
        return self.cost <= other.cost

    def __ge__(self, other) -> bool:
        return self.cost >= other.cost

    def __hash__(self):
        return hash(self.pos)


def output(move):
    print(json.dumps({"move": move}))


_data = json.loads(input())
layout = _data["layout"]

possible_start_positions = []
for i in range(64):
    for j in range(64):
        for rot in range(4):
            possible_start_positions.append((i, j, rot))

pos = None


def is_position_valid(pos, view):
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if rot == 0 and layout[pos[0] + di][pos[1] + dj] != view[1 + di][1 + dj]:
                return False
            elif rot == 1 and layout[pos[0] + di][pos[1] + dj] != view[1 + dj][1 - di]:
                return False
            elif rot == 2 and layout[pos[0] + di][pos[1] + dj] != view[1 - di][1 - dj]:
                return False
            elif rot == 3 and layout[pos[0] + di][pos[1] + dj] != view[1 - dj][1 + di]:
                return False
    return True


net_movement = [0, 0]
net_rotation = 0

goal = None
for i in range(64):
    for j in range(64):
        if layout[i][j] == 2:
            goal = (i, j)

paths = compute_paths(goal)
# print(paths, file=stderr)
# foo

pos = None
rot = None
step_i = 0


def move(dir):
    global net_movement, net_rotation
    net_rotation += dir
    net_rotation = net_rotation % 4
    if dir == 0:
        net_movement = [net_movement[0], net_movement[1]]
        if view[0][1] != 0:
            net_movement[0] += -1
    elif dir == 1:
        net_movement = [net_movement[1], -net_movement[0]]
        if view[1][2] != 0:
            net_movement[0] += -1
    elif dir == 2:
        net_movement = [-net_movement[0], -net_movement[1]]
        if view[2][1] != 0:
            net_movement[0] += -1
    elif dir == 3:
        net_movement = [-net_movement[1], net_movement[0]]
        if view[1][0] != 0:
            net_movement[0] += -1
    output(["forward", "right", "backward", "left"][dir])


while True:
    _data = json.loads(input())
    view = _data["view"]
    view[1][1] = 0

    if len(possible_start_positions) > 1:
        pos_i = 0
        while pos_i < len(possible_start_positions):
            adjusted = list(possible_start_positions[pos_i])

            if net_rotation == 0:
                adjusted[0] += net_movement[0]
                adjusted[1] += net_movement[1]
            elif net_rotation == 1:
                adjusted[0] += net_movement[1]
                adjusted[1] += -net_movement[0]
            elif net_rotation == 2:
                adjusted[0] += -net_movement[0]
                adjusted[1] += -net_movement[1]
            elif net_rotation == 3:
                adjusted[0] += -net_movement[1]
                adjusted[1] += net_movement[0]

            adjusted[2] = (adjusted[2] + net_rotation) % 4

            if not is_position_valid(adjusted, view):
                possible_start_positions.pop(pos_i)
                pos_i -= 1

            if len(possible_start_positions) == 1:
                pos = (adjusted[0], adjusted[1])
                rot = adjusted[2]

            pos_i += 1

        dir = random.randint(0, 3)
        move(dir)

    else:
        path = paths[str(pos)]
        if step_i == len(path):
            print("failure", file=stderr)
            move(0)
        to_move = 0
        if pos[0] < path[step_i][0]:
            to_move = 1
        elif pos[0] > path[step_i][0]:
            to_move = 3
        elif pos[1] < path[step_i][1]:
            to_move = 0
        elif pos[1] > path[step_i][1]:
            to_move = 2
        to_move = (to_move + net_rotation) % 4
        step_i += 1
        move(to_move)
