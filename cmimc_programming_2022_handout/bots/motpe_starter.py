import sys
import json
import random

# INPUT FORMAT (as tower):
'''
    "role": "tower"
    "generator": "uniform" or "circles" or "path"
    "parameter": The difficulty parameter for the generator
        (see problem statement for details). Most simple solutions
        can safely ignore this value.
    "airspace": A 2D (256x256) list of integers representing the grid,
        1 for an unsafe square and 0 for safe. Can be indexed via
        airspace[i][j], where i=255 is the bottom row of the grid.
'''
# OUTPUT FORMAT (as tower):
'''
    "bits": array of 64 0s or 1s, to be passed to your drone.
'''
# Function for handling tower output
def tower_output(bits):
    print(json.dumps({"bits": bits}))



# INPUT FORMAT (as drone):
'''
    "role": "drone"
    "generator": "uniform" or "circles" or "path" (same as above)
    "parameter": difficulty parameter for the generator (same as above)
    "bits": The array of 64 0s or 1s, passed to you by the tower.
'''
# OUTPUT FORMAT (as drone):
'''
    "col": Your starting square in the grid will be airspace[255][col].
    "moves": A string of length at most 2^16 = 65536, consisting of the
        letters "ULDR", denoting moves up, left, down, right,
        to be made in the order sent.
'''
# Function for handling drone output
def drone_output(col, moves):
    print(json.dumps({"col": col, "moves": moves}))



# Fetches input from grader (no need to edit)
_data = json.loads(input())
role = _data["role"]
generator = _data["generator"]
parameter = _data["parameter"]
if role == "tower":
    airspace = _data["airspace"]
if role == "drone":
    bits = _data["bits"]
# End input



## REPLACE STRATEGY BELOW ##

# Sample strategy (random)

if role == "tower":
    # Can read variable "airspace", but not "bits"
    print("airspace", ''.join(map(str, airspace[255])), file = sys.stderr) # example print
    message = random.choices((0, 1), k = 64)
    tower_output(message)

if role == "drone":
    # Can read variable "bits", but not "airspace"
    print("bits", ''.join(map(str, bits)), file = sys.stderr) # example print
    col = random.randint(0, 255)
    moves = random.choices("ULR", k = 65536)
    drone_output(col, moves)
