import sys
import json
import random

# INPUT FORMAT (initial, ONLY HAPPENS ONCE):
'''
    "layout": A 2D (64x64) list of 0, 1, or 2, describing the grid layout,
        where 0 is a floor, 1 is a wall, and 2 is the target destination.
        Can be indexed via layout[i][j].
'''
# INPUT FORMAT (per turn):
'''
    "view": A 2D (3x3) list of 0, 1, or 2, describing the area immediately
        around the robot, oriented in the direction the robot is facing.
        Can be indexed via view[i][j].
'''
# OUTPUT FORMAT (per turn):
'''
    "move": one of "forward", "backward", "left", "right", "apparate"
'''
# Function for handling output
def output(move):
    print(json.dumps({"move": move}))


# You can store globals outside of the main loop
MOVES = ("forward", "backward", "left", "right", "apparate")
size = 64

# Fetches input from grader (no need to edit)
_data = json.loads(input())
layout = _data["layout"]
while True:
    _data = json.loads(input())
    view = _data["view"]
    # End input

    
    ## REPLACE STRATEGY BELOW ##
    
    # Sample strategy (random, moves to the finish if visible)
    can_see_finish = False
    for i in range(3):
        for j in range(3):
            if view[i][j] == 2:
                can_see_finish = True
                print("can see finish (example print)", file = sys.stderr)
                if i == 0: move = 0
                elif i == 2: move = 1
                elif j == 0: move = 2
                elif j == 2: move = 3
    if not can_see_finish: move = random.randint(0, 4)
    output(MOVES[move])
