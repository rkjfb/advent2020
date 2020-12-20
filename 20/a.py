import re
import json
import copy
import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

# edge permutation -> tileid
edge = dict()

# tileid -> tile
tile = dict()

# locked tiles
locked = set()

# grid of tile placements
grid = []

fail = 0

def insert_edges(t, id):
    m = t
    for i in range(4):
        v = m[0,:]
        s = str(v)
        if s in edge:
            #print("fail", s, id, edge[s])
            global fail
            fail += 1
        edge[s] = id
        
        v = np.flip(v)
        s = str(v)
        if s in edge:
            #print("fail")
            fail += 1
        edge[s] = id

        m = np.rot90(m)

tileid = 0
row = []
for line in lines:
    if line == "\n":
        continue

    line = line.strip()

    m = re.search("^Tile (\d*):$", line)
    if not m is None:
        tileid = int(m.group(1))
        y = 0
        row = []
    else:
        d = []
        for c in line:
            if c == '.':
                d.append(0)
            else:
                d.append(1)
        row.append(d)

    if len(row) == 10:
        tile[tileid] = np.array(row)
        insert_edges(tile[tileid], tileid)

# populate grid with zeros
s = int(math.sqrt(len(tile)))

for x in range(s):
    grid.append([0] * s)


print(len(tile))
print(grid)
print("fail", fail)


