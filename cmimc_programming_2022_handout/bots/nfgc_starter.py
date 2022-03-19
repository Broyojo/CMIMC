import sys
import json
import random

# INPUT FORMAT (per turn):
'''
    "yesterday": [] on first day, otherwise a 2D list, where each element is
        [c_1, c_2, ..., c_10] for a specific player.
        The order of the players remains consistent in this list.
    "scores": A list of all players’ current total money made.
        The order of the players here matches that of "yesterday".
    "my_index": Which index into the above lists you are.
'''
# OUTPUT FORMAT (per turn):
'''
    "buys": A list [c_1, c_2, ..., c_10] of how many of each coin
        you would like to purchase, which must be non-negative integers
        summing to at most 100.
'''
# Function for handling output
def output(buys):
    print(json.dumps({"buys": buys}))


# You can store globals outside of the main loop
my_history = []
day = 0

while True:
    # Fetches input from grader (no need to edit)
    _data = json.loads(input())
    yesterday = _data["yesterday"]
    scores = _data["scores"]
    my_index = _data["my_index"]
    # End input

    
    ## REPLACE STRATEGY BELOW ##
    
    # Sample strategy (random)
    if day == 0: assert yesterday == [] # yesterday is empty on first day
    my_score = scores[my_index]
    if day == 29: print("final score", my_score, file = sys.stderr) # example print
    
    buys = [0] * 10
    dividers = [0] + sorted(random.choices(range(101), k = 9)) + [100]
    for i in range(10):
        buys[i] = dividers[i+1] - dividers[i]
    my_history.append(buys)
    output(buys)
    day += 1
