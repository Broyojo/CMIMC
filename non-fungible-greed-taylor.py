import json
from math import factorial
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

def buy(buys):
    print(json.dumps({"buys": buys}))

history = []
day = 0

while True:
    # read data
    _data = json.loads(input())
    yesterday = _data["yesterday"]
    scores = _data["scores"]
    my_index = _data["my_index"]
    
    if day == 0:
        # an arbitrary first day strategy based on typical first days (grabbed from replays)
        buys = [0 for _ in range(10)]
        purchases = [88,100,95,145,223,280,307,288,319,446]
        for _ in range(100):
            expected_benefit = [ ((i+1) * ((buys[i]+1) / (purchases[i]+buys[i]+1) - buys[i] / (purchases[i]+buys[i]))) if purchases[i]+buys[i] != 0 else i+1 for i in range(10)]
            to_buy = expected_benefit.index(max(expected_benefit))
            buys[to_buy] += 1
        buy(buys)
        day += 1
    else:
        # 1. aggregate yesterday's purchases
        yesterday_sums = [0 for _ in range(10)]
        for i, move in enumerate(yesterday):
            if i != my_index:
                for coin in range(len(move)):
                    yesterday_sums[coin] += move[coin]
        history.append(yesterday_sums)
        
        # 2. compute a newton series (Taylor Series but discrete) for every coin
        coin_series = []
        for coin_i in range(10):
            # 2a. compute the backward-finite difference derivatives (https://en.wikipedia.org/wiki/Finite_difference)
            derivatives = [[history[i][coin_i] for i in range(day)]]
            while len(derivatives[-1]) != 1 and len(derivatives) < 3:
                derivatives.append([derivatives[-1][i+1] - derivatives[-1][i] for i in range(len(derivatives[-1]) - 1)])

            def upward_factorial(n, terms):
                return '*'.join([f"({n}+{i-day+1})" for i in range(terms)])

            # 2b. compute the series (also https://en.wikipedia.org/wiki/Finite_difference)
            series = ""
            for term_i, derivative in enumerate(derivatives):
                derivative = derivative[-1]
                if term_i > 0:
                    series += f"{derivative}*{upward_factorial('x',term_i)}/{factorial(term_i)} + "
                else:
                    series += str(derivative) + " + "
            series = series[:-3]
            coin_series.append(series)
        
        # 3. evaluate the series to get a prediction for today
        prediction = []
        for series in coin_series:
            value = max(0, eval(series.replace("x", str(day))))
            prediction.append(value)
        print(f"I predict {prediction}", file=stderr)
        
        # 4. select optimal purchases based on the prediction
        buys = [0 for _ in range(10)]
        for _ in range(100):
            expected_benefit = [ ((i+1) * ((buys[i]+1) / (prediction[i]+buys[i]+1) - buys[i] / (prediction[i]+buys[i]))) if prediction[i]+buys[i] != 0 else i+1 for i in range(10)]
            to_buy = expected_benefit.index(max(expected_benefit))
            buys[to_buy] += 1

        buy(buys)
        day += 1
    
    if day == 30: print("final score (real)", scores[my_index], file = stderr)