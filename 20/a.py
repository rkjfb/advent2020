import re
import json
import copy
import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

# edge_owner -> set(tileid)
# permutation of all edges of all tiles -> [tileid]
edge_owner = dict()

# id -> [neighbours]
edge = dict()

# tileid -> tile
tile = dict()

# corner tiles
corner_t = set()
# edge tiles
edge_t = set()
# center tiles
center_t = set()

# grid of tile placements
grid = []

def insert_edge(s, id):
    if not s in edge_owner:
        edge_owner[s] = []
    if not id in edge_owner[s]:
        edge_owner[s].append(id)

# permutes edges
def insert_edges(t, id):
    m = t
    for i in range(4):
        v = m[0,:]
        insert_edge(str(v), id)
        
        v = np.flip(v)
        insert_edge(str(v), id)

        m = np.rot90(m)

# updates edge
def update_edges():
    global edge
    for k,v in edge_owner.items():
        if len(v) == 2:
            t1 = v[0]
            t2 = v[1]

            if not t1 in edge:
                edge[t1] = []
            if not t2 in edge[t1]:
                edge[t1].append(t2)

            if not t2 in edge:
                edge[t2] = []
            if not t1 in edge[t2]:
                edge[t2].append(t1)

# returns corners 
def update_positions():
    for k,v in edge.items():
        if len(v) == 2:
            corner_t.add(k)
        elif len(v) == 3:
            edge_t.add(k)
        elif len(v) == 4:
            center_t.add(k)
        else:
            print("unrecognized tile", k, v)

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

update_edges()
update_positions()

# populate grid with zeros
s = int(math.sqrt(len(tile)))

for x in range(s):
    grid.append([0] * s)

# if we've bucketed correct, tile count should be unchanged
assert len(tile) == len(corner_t) + len(edge_t) + len(center_t)


print(len(tile))
print(grid)
print("corners", len(corner_t))
print("edges", len(edge_t))
print("centers", len(center_t))

product = 1
for e in corner_t:
    product *= e

print(product)



