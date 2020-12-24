import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

# 2d co-ord, starting at (0,0)
#    nw -1,1 /\ ne 1,  1 
#   w -2, 0 |xx| e 2,  0
#  sw -1, -1 \/ se 1, -1 

offset = { "nw": [-1,1],
           "ne" : [1,1],
            "w" : [-2,0],
            "e" : [2,0],
            "sw" : [-1,-1],
            "se" : [1,-1] }

tiles = dict()

for line in lines:
    if line == "\n":
        continue

    line = line.strip()

    pos = [0,0]

    while len(line) > 0:
        o = None
        if len(line) > 1:
            cc = line[0:2]
            if cc in offset:
                o = offset[cc]
                line = line[2:]
        if o == None:
            c = line[0:1]
            if c in offset:
                o = offset[c]
                line = line[1:]
        if o == None:
            print("unrecognized", line)

        pos[0] += o[0]
        pos[1] += o[1]

    k = str(pos)
    if k in tiles:
        tiles[k] = not tiles[k]
    else:
        tiles[k] = True

print(tiles)

count = 0
for k in tiles:
    if tiles[k]:
        count += 1
print("count", count)
