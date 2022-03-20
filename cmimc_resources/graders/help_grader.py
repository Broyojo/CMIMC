from local_test_framework import OptGrader

import random
import itertools
from collections import defaultdict

class Help(OptGrader):
    name = "help"

    def footprint(self, grid, x, y):
        delta = ((-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0))
        values = [0]
        for i in range(8):
            dx, dy = delta[i]
            values[0] += grid[y + dy][x + dx] << i
        for i in range(3):
            values.append(((values[-1] & 3) << 6) + (values[-1] >> 2))
        return min(values)

    def special_dfs(self, grid, size, finish_x, finish_y):
        delta = ((1,0), (0,1), (-1,0), (0,-1))
        footprints = defaultdict(list)
        for x, y in itertools.product(range(size), repeat = 2):
            if not grid[y][x]:
                footprints[self.footprint(grid, x, y)].append((x, y))
        visited = [[0] * size for i in range(size)]
        start = (finish_x, finish_y)
        visited[start[1]][start[0]] = 1
        q = [start]
        while q:
            x, y = q.pop()
            for dx, dy in delta:
                nx, ny = x + dx, y + dy
                if not grid[ny][nx] and not visited[ny][nx]:
                    visited[ny][nx] = 1
                    q.append((nx, ny))
            for nx, ny in footprints[self.footprint(grid, x, y)]:
                if not grid[ny][nx] and not visited[ny][nx]:
                    visited[ny][nx] = 1
                    q.append((nx, ny))
        return visited

    def make_maze(self, size = 64, density = .5, count = 16, r = 3):
        array = [[random.random() < density for x in range(size)] for y in range(size)]
        for i in range(count):
            x, y = random.randint(r, size - 1 - r), random.randint(r, size - 1 - r)
            for dx, dy in itertools.product(range(-r, r + 1), repeat = 2):
                if dx * dx + dy * dy < r * r:
                    nx, ny = x + dx, y + dy
                    array[-1 - ny][nx] = 0
        for i in range(size):
            array[0][i] = array[i][0] = array[-1][i] = array[i][-1] = 1
        finish = False
        while not finish:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            for dx, dy in itertools.product(range(-2, 3), repeat = 2):
                nx, ny = x + dx, y + dy
                if array[ny][nx]: break
            else:
                finish_x, finish_y = x, y
                finish = True
        reachable = self.special_dfs(array, size, finish_x, finish_y)
        for x, y in itertools.product(range(size), repeat = 2):
            if not array[y][x] and not reachable[y][x]: array[y][x] = 1
        array[finish_y][finish_x] = 2
        return array
    
    config = {
        'timeout': 5,
        'cputime': 5,
        'walltime': 60,
        'memlimit': 256 << 20,
    }

    def get_batch(self, task):
        random.seed()
        return [
            (None, random.randrange(1 << 30))
            for _ in range(10)]
    
    def optgrade(self, gen, code):
        board = self.make_maze()
        board = [[int(x) for x in row] for row in board]
        trail = []

        # clockwise order
        deltas = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

        def around(i, j, rot):
            ret = [[0 for _ in range(3)] for _ in range(3)]
            shifted = deltas[2*rot:] + deltas[:2*rot]
            for (oi,oj),(si,sj) in zip(deltas,shifted):
                what = 1
                fi,fj = i+si,j+sj
                if 0 <= fi < 64 and 0 <= fj < 64:
                    what = board[fi][fj]
                ret[oi+1][oj+1] = what
            ret[1][1] = board[i][j]
            return ret
        
        def around_t(i, j, rot):
            return tuple(sum(around(i,j,rot),[]))
        
        tp = defaultdict(list)
        for i in range(64):
            for j in range(64):
                if board[i][j] != 0: continue
                for rot in range(4):
                    tp[around_t(i,j,rot)].append( (i,j,rot) )

        code.write({ 'layout': board })

        possible_starts = []
        for i in range(64):
            for j in range(64):
                if board[i][j] == 0 and 2 not in sum(around(i,j,0), []):
                    possible_starts.append( (i,j) )
        
        starti, startj = random.choice(possible_starts)
        startrot = random.randrange(4)
        
        i,j,rot = starti,startj,startrot
        score = 0
        for move_no in range(4096):
            trail.append( (i,j,rot) )
            code.write({ 'view': around(i, j, rot) })

            shifted = deltas[2*rot:] + deltas[:2*rot]

            move = "forward"
            try:
                move = str(code.read()['move'])
            except:
                pass
            if move == "backward":
                offset = 2
            elif move == "right":
                offset = 1
            elif move == "left":
                offset = 3
            elif move == "forward":
                offset = 0
            else: # move == "apparate"
                offset = None
                ind = around_t(i, j, rot)
                if 1 in ind:
                    i,j,rot = random.choice(tp[ind])
            
            if offset is not None:
                di,dj = shifted[2*offset]
                newi,newj = i+di,j+dj
                if 0 <= newi < 64 and 0 <= newj < 64 and board[newi][newj] != 1:
                    i,j = newi,newj
                rot = (rot + offset) % 4

            if board[i][j] == 2:
                score = 4096 / (move_no + 64)
                trail.append( (i,j,rot) )
                break

        return {
            'summary': score,
            'history': {
                'board': board,
                'trail': trail,
            },
            'playerlogs': code.interaction_log(),
        }
