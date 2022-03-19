import json
from math import sqrt
from sys import stderr

# INPUT FORMAT (per turn):

# "yesterday": [] on first day, otherwise a 2D list, where each element is
#     [c_1, c_2, ..., c_10] for a specific player.
#     The order of the players remains consistent in this list.
# "scores": A list of all players’ current total money made.
#     The order of the players here matches that of "yesterday".
# "my_index": Which index into the above lists you are.

# OUTPUT FORMAT (per turn):
# "buys": A list [c_1, c_2, ..., c_10] of how many of each coin
#     you would like to purchase, which must be non-negative integers
#     summing to at most 100.

class Strategy():
    def make_purchases(self, yesterday, scores, self_index):
        pass
    
    def agrees_with(self, history, scores, self_index):
        # this determines how well this strategy represents an opponent's actions thus far

        # 1. aggregate my moves
        moveset = []
        for day in range(len(history)):
            moveset.append(history[day][self_index])
        
        # 2. run a simulation of this strategy's moves
        predicted_moveset = []
        for day in range(len(history)):
            yesterday = []
            if day != 0:
                yesterday = history[day-1]
                predicted_move = self.make_purchases(yesterday, scores, self_index)
            else:
                predicted_move = [10 for _ in range(10)]
            predicted_moveset.append(predicted_move)

        # 3. compute the mean squared error between the simulated moves and the opponent's actual moves
        mse = 0
        for day in range(len(history)):
            predicted_move = predicted_moveset[day]
            move = moveset[day]
            
            for coin_i in range(len(move)):
                dif = move[coin_i] - predicted_move[coin_i]
                mse += dif**2 * sqrt(day + 1) # weight the later days more to compensate for addaptive algorithms
        mse /= 10 * len(history)
    
        return mse

class GreedyOneAhead(Strategy):
    def make_purchases(self, yesterday, scores, self_index):
        buys = [0 for _ in range(10)]
        # 1. aggregate a list of how much each coin was purchased
        purchases = [0 for _ in range(10)]
        for i, move in enumerate(yesterday):
            if i != self_index:
                for coin in range(len(move)):
                    purchases[coin] += move[coin]
        
        # 2. repeatedly select the coin with the highest expected value
        for _ in range(100):
            expected_benefit = [ (i+1) * ((buys[i]+1) / (purchases[i]+buys[i]+1) - buys[i] / (purchases[i]+buys[i])) if purchases[i]+buys[i] != 0 else i+1 for i in range(10)]
            to_buy = expected_benefit.index(max(expected_benefit))
            buys[to_buy] += 1
        
        return buys

class NoChange(Strategy):
    def make_purchases(self, yesterday, scores, self_index):
        buys = yesterday[self_index]
        return buys

class PickLeast(Strategy):
    def make_purchases(self, yesterday, scores, self_index):
        buys = [0 for _ in range(10)]
        
        # 1. aggregate a list of how much each coin was purchased
        purchases = [0 for _ in range(10)]
        for i, move in enumerate(yesterday):
            if i != self_index:
                for coin in range(len(move)):
                    purchases[coin] += move[coin]
        
        # 2. find the least purchased coin
        least_i = purchases.index(min(purchases))
        buys[least_i] = 100

        return buys

strategies = [GreedyOneAhead(), NoChange(), PickLeast()]
def buy(buys):
    print(json.dumps({"buys": buys}))

def classify_opponents(history, scores, my_index):
    classifications = []
    for opponent_i in range(len(history[0])):
        if opponent_i == my_index:
            classifications.append(None)
        else:
            strategy_scores = []
            for strategy in strategies:
                strategy_scores.append(strategy.agrees_with(history, scores, opponent_i))
            best = strategy_scores.index(min(strategy_scores))
            classifications.append(strategies[best])
    return classifications

history = []
day = 0

while True:
    # read data
    _data = json.loads(input())
    yesterday = _data["yesterday"]
    scores = _data["scores"]
    my_index = _data["my_index"]
    
    if day == 0:
        # an arbitrary first day strategy
        buys = [10 for _ in range(10)]
        buy(buys)
        day += 1
    else:
        # attempt to classify the opponent's behavior
        history.append(yesterday)
        opponent_strategies = classify_opponents(history, scores, my_index)
        
        # simulate opponent's moves
        today_prediction = yesterday
        for opponent_i in range(len(today_prediction)):
            if opponent_i != my_index:
                opponent_strat = opponent_strategies[opponent_i]
                print(f"opponent {opponent_i+1} will probably buy {opponent_strat.make_purchases(yesterday, scores, opponent_i)}", file = stderr)
                today_prediction[opponent_i] = opponent_strat.make_purchases(yesterday, scores, opponent_i)
        
        # buy coins based on opponent's moves
        buys = GreedyOneAhead().make_purchases(today_prediction, scores, my_index)
        print(f"I will buy {buys}", file = stderr)
        
        buy(buys)
        day += 1
    
    if day == 30: print("final score (real)", scores[my_index], file = stderr)