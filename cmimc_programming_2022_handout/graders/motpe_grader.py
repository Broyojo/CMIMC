from local_test_framework import OptGrader

import random
import math
import itertools

class MotPE(OptGrader):
    name = "motpe"

    def make_random(self, size = 256, parameter = 10):
        density = parameter / 100
        array = [[random.random() < density for x in range(size)] for y in range(size)]
        return array

    def make_circles(self, size = 256, parameter = 4, r_lo = 4, r_hi = 32):
        gap = parameter
        radius = 2 * r_hi
        array = [[0] * size for i in range(size)]
        tries = 1000
        while radius > 2 * r_lo:
            r = radius // 2
            R = r + gap
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            for dx, dy in itertools.product(range(-R, R + 1), repeat = 2):
                if dx * dx + dy * dy < R * R:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        if array[-1 - ny][nx]:
                            tries -= 1
                            if not tries:
                                radius -= 1
                                tries = 1000
                            break
            else:
                for dx, dy in itertools.product(range(-r, r + 1), repeat = 2):
                    if dx * dx + dy * dy < r * r + r:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < size and 0 <= ny < size:
                            array[-1 - ny][nx] = 1
                radius -= 1
        return array

    def random_poly00(self, roots, radius, steps = 10000):
        sign = random.randint(0,1) * 2 - 1
        def f(x):
            p = x * (x - 1)
            for r in roots: p *= x - r
            return sign * p
        m = 0
        for i in range(steps):
            x = i / steps
            y = abs(f(x))
            if y > m: m = y
        def g(x):
            return radius * f(x) / m
        return g

    def random_poly01(self, roots, radius, steps = 10000):
        def f(x):
            p = x * (x - 1)
            for r in roots: p *= x - r
            return p
        m = 0
        for i in range(steps):
            x = i / steps
            y = abs(f(x))
            if y > m: m = y
        within_bounds = False
        extra = 1
        while not within_bounds:
            def g(x):
                return abs(.5 * radius * f(x) / m + x ** extra * radius)
            for i in range(steps):
                x = i / steps
                y = g(x)
                if y > radius:
                    extra += 1
                    break
            else: within_bounds = True
        return g

    def make_path(self, size = 256, parameter = 16, height = 2, steps = 10000):
        width = parameter // 2
        array = [[1] * size for i in range(size)]
        points = [[0] * size for i in range(size)]
        x_lo, x_hi = size, size
        for h in range(height):
            roots1 = [random.random() for i in range(4)]
            roots2 = [random.random() for i in range(3)]
            fx = self.random_poly00(roots1, size // 2 - 5 * width)
            fy = self.random_poly01(roots2, size // height)
            for i in range(steps):
                t = i / steps
                x = size // 2 + math.floor(fx(t))
                if x < x_lo: x_lo = x
                if size - 1 - x < x_hi: x_hi = size - 1 - x
                y = math.floor(fy(t)) + h * (size // height)
                points[-1 - y][x] = 1
        offset1, offset2 = random.randint(-x_lo, x_hi), random.randint(-x_lo, x_hi)
        for x, y in itertools.product(range(size), repeat = 2):
            if points[y][x]:
                offset = (offset1 * y + offset2 * (size - y)) // size
                for dx, dy in itertools.product(range(-width, width + 1), repeat = 2):
                    if dx * dx + dy * dy < width * width:
                        nx, ny = x + dx + offset, y + dy
                        if 0 <= nx < size and 0 <= ny < size:
                            array[-1 - ny][nx] = 0
        return array

    config = {
        'timeout': 10,
        'cputime': 10,
        'walltime': 60,
        'memlimit': 256 << 20,
    }

    def get_batch(self, task):
        random.seed()
        generator_types = ["random", "circles", "path"]
        assert task in generator_types
        difficulties = {
            "random" : [6,7,8,9,10,11,12,13,14,15],
            "circles" : [10,9,8,7,6,6,5,4,3,2],
            "path" : [22,20,18,18,16,16,14,14,12,10]
        }
        return [((task, difficulties[task][i]), random.randrange(1 << 30)) for i in range(10)]
    
    def optgrade(self, gen, code):
        gens = {
            "path": self.make_path,
            "circles": self.make_circles,
            "random": self.make_random,
        }
        gen_name, difficulty = gen
        gen = gens[gen_name]
        board = gen(parameter = difficulty)
        board = [[int(x) for x in row] for row in board]
        code.write({'role': 'tower', 'airspace': board, 'generator': gen_name, 'parameter': difficulty})
        bits = [0] * 64
        try:
            cand = code.read()
            arr = cand["bits"]
            for i in range(64):
                j = int(arr[i])
                assert j in (0,1)
                bits[i] = j
        except:
            pass
        code.restart()
        code.write({'role': 'drone', 'bits': bits, 'generator': gen_name, 'parameter': difficulty})
        starting_col = 0
        moves = ""
        try:
            response = code.read()
            cand_col = int(response["col"])
            assert 0 <= cand_col < 256
            starting_col = cand_col
            cand_moves = response["moves"][:1 << 16]
            assert(all(m in ("U","D","L","R") for m in cand_moves))
            moves = cand_moves
        except:
            pass

        score = 0
        i, j = 255, starting_col

        def check():
            nonlocal score
            if 0 <= i < 256 and 0 <= j < 256 and not board[i][j]:
                score = max(score, 256 - i)
                return True
            else:
                return False

        time = 0
        while check() and time < len(moves):
            m = moves[time]
            if m == "U": i -= 1
            elif m == "D": i += 1
            elif m == "L": j -= 1
            elif m == "R": j += 1
            else: assert(False)
            time += 1

        return {
            'summary': score,
            'history': {
                'board': board,
                'bits': bits,
                'col': starting_col,
                'moves': moves,
            },
            'playerlogs': code.interaction_log(),
        }
