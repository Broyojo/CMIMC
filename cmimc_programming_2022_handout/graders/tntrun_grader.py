from local_test_framework import AIGrader
import copy

class TNTRun(AIGrader):
    name = "tntrun"

    config = {
        'timeout': 2,
        'cputime': 2,
        'walltime': 60,
        'memlimit': 256 << 20,
    }

    def aigrade(self, players):
        size = 25
        board = [[1 for _ in range(size)] for _ in range(size)]
        grace_moves_left = 6
        pos = [{ 'i': 12, 'j': 12, 'alive': True } for p in players]
        summary = [0 for p in players]
        history = []

        move_number = 0
        changing = True
        while changing:
            changing = False
            state = {
                'arena': copy.deepcopy(board),
                'players': pos,
                'grace_moves_left': grace_moves_left
            }
            history.append(copy.deepcopy(state))
            for p in pos:
                if not p['alive']: continue
                changing = True
                if not grace_moves_left: board[p['i']][p['j']] = 0
            for i,p in enumerate(players):
                if not pos[i]['alive']: continue
                p.write({**state, 'my_index': i})
                newi, newj = pos[i]['i'], pos[i]['j']
                try:
                    res = p.read()
                    candi = int(res['i'])
                    candj = int(res['j'])
                    assert abs(newi - candi) <= 2
                    assert abs(newj - candj) <= 2
                    assert 0 <= candi <= size
                    assert 0 <= candj <= size
                    assert board[candi][candj]
                    newi, newj = candi, candj
                except:
                    pass
                pos[i]['i'] = newi
                pos[i]['j'] = newj
                if not board[newi][newj]:
                    summary[i] = move_number
                    pos[i]['alive'] = False
            if grace_moves_left: grace_moves_left -= 1
            move_number += 1
        return {
            'history': history,
            'summary': summary,
            'playerlogs': [p.interaction_log() for p in players]
        }
