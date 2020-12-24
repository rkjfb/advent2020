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

def get_count():
    count = 0
    for k in tiles:
        if tiles[k]:
            count += 1
    return count

def day():
    global tiles
    n = dict()

    # fill in implied whites, to simplify neighbour counting
    addme = []
    for k in tiles:
        if tiles[k]:
            x,y = k
            for ok,ov in offset.items():
                check = (x+ov[0], y+ov[1])
                if not check in tiles:
                    addme.append(check)
    for a in addme:
        tiles[a] = False

    # count neighbours
    for k in tiles:
        true_count = 0
        false_count = 0
        x,y = k
        for ok,ov in offset.items():
            check = (x+ov[0], y+ov[1])
            if not check in tiles:
                false_count += 1
            elif tiles[check]:
                true_count += 1
            else:
                false_count += 1
        
        # blindly copy
        n[k] = tiles[k]

        if tiles[k] and (true_count == 0 or true_count > 2):
            n[k] = False

        if not tiles[k] and true_count == 2:
            n[k] = True

    tiles = n


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

    k = (pos[0], pos[1])
    if k in tiles:
        tiles[k] = not tiles[k]
    else:
        # True == black
        # False = unspecified = default = white
        tiles[k] = True


print("initcount", get_count())
for i in range(100):
    day()
    print(i+1, get_count())
