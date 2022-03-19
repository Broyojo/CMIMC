import json

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
    my_history.append(buys)
    print(json.dumps({"buys": buys}))

my_history = []
day = 0

while True:
    # read data
    _data = json.loads(input())
    yesterday = _data["yesterday"]
    scores = _data["scores"]
    my_index = _data["my_index"]
    
    # the actual strategy
    buys = [0 for _ in range(10)]
    if day == 0:
        # an arbitrarily selected first day strategy
        buys = [0,0,0,0,0,0,0,0,0,100]
    else:
        # the actual strategy

        # 1. aggregate a list of how much each coin was purchased
        purchases = [0 for _ in range(10)]
        for i, move in enumerate(yesterday):
            if i != my_index:
                for coin in move:
                    purchases[coin] += move[coin]
        
        # 2. repeatedly select the coin with the highest expected value
        for _ in range(100):
            expected_benefit = [i/purchases[i] for i in range(10)]
            to_buy = expected_benefit.index(max(expected_benefit))
            buys[to_buy] += 1
            purchases[to_buy] += 1
    
    buy(buys)
    day += 1
