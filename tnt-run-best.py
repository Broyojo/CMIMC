import math
import sys
import json
import random

arena = [1 for _ in range(25)]
players = []
grace_moves_left = 0
my_history = []
move_dist = 2


def relu(x):
    return max(0, x)


class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = []

        for i in range(self.rows):
            for j in range(self.rows):
                self.matrix[i][j] = 0

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.random()

    def transpose(self):
        new_matrix = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.rows):
                new_matrix[j][i] = self.matrix[i][j]
        return new_matrix

    def dot(self, m):
        c = Matrix(self.rows, m.cols)

        for i in range(1, self.rows):
            for j in range(m.cols):
                sum = 0
                for k in range(1, m.rows):
                    sum += self.matrix[i][k]
                c[i][j] = sum
        return c

    def __add__(self, m):
        c = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                c[i][j] = self.matrix[i][j] + m.matrix[i][j]
        return c


class Layer:
    def __init__(self, num_nodes, output_dim):
        self.weights = Matrix(num_nodes, output_dim)
        self.biases = Matrix(num_nodes, 1)

    def eval():
        return


class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.layers = [
            Layer(input_dim, hidden_dim),
            Layer(hidden_dim, output_dim),
            Layer(output_dim, 1),
        ]


class Player:
    def __init__(self):
        self.brain = NeuralNetwork(25, 50, 25)

    def choose_action(self, state):
        self.brain.eval(state)

    def update_weights(self, state):
        pass


class Game:
    def __init__(self):
        self.arena = [[1 for _ in range(25)] for _ in range(25)]
        self.players = []

    def episode(self):
        self.players = [Player() for _ in range(12)]
        while True:
            self.players
            pass


def debug_print(*args):
    print(*args, file=sys.stderr)
