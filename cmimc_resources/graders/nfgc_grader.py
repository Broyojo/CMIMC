from local_test_framework import AIGrader

class NFGC(AIGrader):
    name = "nfgc"
    coins = 10
    spending = 100
    rounds = 30

    config = {
        'timeout': 3,
        'cputime': 3,
        'walltime': 60,
        'memlimit': 100 << 20,
    }

    def aigrade(self, players):
        decisions = []
        yesterday = []
        scores = [0 for p in players]
        def turn(player, yesterday, scores, index):
            player.write({
                'yesterday': yesterday,
                'scores': scores,
                'my_index': index
            })
            move = [0] * self.coins
            try:
                turn = player.read()
                buys = turn["buys"]
                left = self.spending
                for i in range(self.coins):
                    user_val = int(buys[i])
                    assert 0 <= user_val <= left
                    left -= user_val
                    move[i] = user_val
            except:
                pass
            return move
        for _ in range(self.rounds):
            yesterday = [turn(players[i], yesterday, scores, i) for i in range(len(players))]
            decisions.append(yesterday)
            total = [0] * self.coins
            for t in yesterday:
                for i in range(self.coins):
                    total[i] += t[i]
            for p in range(len(players)):
                for i in range(self.coins):
                    if total[i]:
                        scores[p] += (i+1) * yesterday[p][i] / total[i]
        return {
            'history': decisions,
            'summary': scores,
            'playerlogs': [p.interaction_log() for p in players]
        }
