import sys
import json
import random

# INPUT FORMAT (per turn):
'''
    "arena": A 2D (25 x 25) list of integers representing the current
        arena state, 1 for a present tile and 0 for empty.
        Can be indexed via arena[i][j].
    "players": For every player, a dict containing
        "alive": whether they are alive or dead.
        "i", "j": their zero-indexed coordinates.
        The order of the players remains consistent in this list.
    "my_index": Which index into the "players" list you are.
    "grace_moves_left": How many grace moves are remaining (if any),
        i.e. if this is 1, then on your next move, the ground currently
        underneath you does not disappear, but if this is 0 it does.
'''
# OUTPUT FORMAT (per turn):
'''
    "i", "j": Your destination coordinates. Each coordinate can differ by
        at most 2 from your previous coordinates.
'''
# Function for handling output
def output(i, j):
    print(json.dumps({"i": i, "j": j}))


# You can store globals outside of the main loop
my_history = []
size = 25
print("example print", file = sys.stderr)

while True:
    # Fetches input from grader (no need to edit)
    _data = json.loads(input())
    arena = _data["arena"]
    players = _data["players"]
    my_index = _data["my_index"]
    grace_moves_left = _data["grace_moves_left"]
    # End input

    
    ## REPLACE STRATEGY BELOW ##
    
    # Sample strategy (random)
    me = players[my_index]
    me_i, me_j = me["i"], me["j"]
    my_history.append((me_i, me_j))
    
    new_i, new_j = -1, -1
    while not (0 <= new_i < size and 0 <= new_j < size):
        di, dj = random.randint(-2, 2), random.randint(-2, 2)
        new_i, new_j = me_i + di, me_j + dj
    output(new_i, new_j)
