import sys
import json
import random


def log(*args):
    print(*args, file=sys.stderr)


airspace = []
bits = []
_data = json.loads(input())
role = _data["role"]
generator = _data["generator"]
parameter = _data["parameter"]
if role == "tower":
    airspace = _data["airspace"]
    log("length of airspace:", len(airspace))
if role == "drone":
    bits = _data["bits"]
size = 256


bits_for_starting_pos = 8  # 2^8 = 256
# 56 bits left, 8 possible moves
bits_for_movement = 5     # 2^5 = 32
bits_for_turn = 2         # 2^2 = 4

UP = 0
RIGHT = 1
LEFT = 2


class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def is_valid(self):
        return 0 <= self.i <= size-1 and 0 <= self.j <= size-1 and airspace[self.i][self.j] == 0

    def __add__(self, p):
        return Point(self.i + p.i, self.j + p.j)

    def __str__(self):
        return f"({self.i}, {self.j})"

    def __repr__(self):
        return str(self)


class PathFinder:
    def __init__(self, airspace, size):
        pass

    def find_optimal_path(self):
        pass


class Encoder:
    def __init__(self, max_size):
        pass


class Game:
    def __init__(self, data):
        # data from the environment
        self.generator = data["generator"]
        self.role = data["role"]
        self.parameter = data["parameter"]
        self.airspace = data["airspace"] if self.role == "tower" else []
        self.bits = data["role"] if self.role == "drone" else []
        self.max_msg_size = 64

        # how many bits per piece of information
        self.start_pos_bits = 8
        self.movement_bits = 5
        self.turn_bits = 2

        # directions
        self.UP = 0
        self.RIGHT = 1
        self.LEFT = 2

        self.path_finder = PathFinder(airspace)
        self.encoder = 2

# def main():
#     game = Game(
# main()


# moves are (dir, length)


class Move:
    def __init__(self, dir, dist):
        self.dir = dir
        self.dist = dist

    def __str__(self):
        d = ""
        if dir == UP:
            s = "UP"
        elif dir == RIGHT:
            s = "RIGHT"
        elif dir == LEFT:
            s = "LEFT"
        return f"move {self.dist} {d}"


class Path:
    def __init__(self, start):
        self.start = start
        self.moves = []
        self.score = 0

    def add_move(self, move):
        if move[0] == UP:  # if we go up
            self.score += move[0]
        self.moves.append(move)

    def remove_move(self):
        self.moves.pop()

    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return self.score != other.score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __len__(self):
        return len(self.moves)

    def __str__(self):
        s = ""
        for move in self.moves:
            s += str(move) + " -> "
        return s


def find_paths(p, moves, initial_moves, score=0, mem=[]):
    if moves == 0:
        return score
    if p in mem:
        return score
    paths = [[]]
    print("Moves left:", moves, file=sys.stderr)
    for dir in range(3):
        print("Direction is", dir, file=sys.stderr)
        if dir == UP:
            max_distance = 0
            while Point(p.i - max_distance, p.j).is_valid():
                max_distance += 1
            for distance in range(max_distance, 0, -1):
                print("Testing distance:", distance, file=sys.stderr)
                new_p = Point(p.i - distance, p.j)
                score += distance
                mem.append(new_p)
                paths[-1].append(find_paths(new_p, moves-1,
                                            initial_moves, score, mem))
        elif dir == RIGHT:
            max_distance = 0
            while Point(p.i, p.j + max_distance).is_valid():
                max_distance += 1
            for distance in range(max_distance, 0, -1):
                new_p = Point(p.i - distance, p.j)
                mem.append(new_p)
                paths.append(find_paths(new_p, moves-1,
                             initial_moves, score, mem))
        elif dir == LEFT:
            max_distance = 0
            while Point(p.i, p.j - max_distance).is_valid():
                max_distance += 1
            for distance in range(max_distance, 0, -1):
                new_p = Point(p.i - distance, p.j)
                mem.append(new_p)
                paths.append(find_paths(new_p, moves-1,
                             initial_moves, score, mem))
    print("Points in mem:", mem, file=sys.stderr)
    return paths


def find_optimal_path():
    best_path = Path(Point(0, 0))
    for start_col_index in airspace[255]:
        if start_col_index == 0:
            paths = find_paths(Point(255, start_col_index))
            for path in paths:
                if path > best_path:
                    best_path = path


def tower_output(bits):
    print(json.dumps({"bits": bits}))


def drone_output(col, moves):
    print(json.dumps({"col": col, "moves": moves}))


if role == "tower":
    print("airspace", ''.join(map(str, airspace[255])), file=sys.stderr)
    message = []
    print("Paths:", find_paths(Point(255, 0), 8), file=sys.stderr)
    print("hello", file=sys.stderr)
    tower_output(message)

if role == "drone":
    print("bits", ''.join(map(str, bits)), file=sys.stderr)
    col = random.randint(0, 255)
    moves = random.choices("ULR", k=65536)
    drone_output(col, moves)


def main():
    data = json.loads(input())
    game = Game(data)


main()
