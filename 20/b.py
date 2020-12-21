import re
import json
import copy
import numpy as np
from collections import deque
import math
import sys

# print bigger matrices
np.set_printoptions(threshold=sys.maxsize)

data = open("data.txt", "r")
lines = data.readlines()

# edge_owner -> set(tileid)
# permutation of all edges of all tiles -> [tileid]
edge_owner = dict()

# (t1,t2) -> v
common_edge = dict()

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

            # remember common edge
            common_edge[(min(t1,t2),max(t1,t2))] = k

def get_common_edge(t1,t2):
    return common_edge[min(t1, t2), max(t1, t2)]

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

# returns list of all tile positions
def tile_permutes(id):
    ret = []
    m = tile[id]
    for i in range(4):
        m = np.rot90(m)
        ret.append(m)
    m = np.fliplr(tile[id])
    for i in range(4):
        m = np.rot90(m)
        ret.append(m)
    return ret

# spins tile id until right column matches v
def orient_tile_right(id, v):
    dbg = False
    if id == 12345:
        dbg = True
        print("goal", v)

    count = 0
    perm = tile_permutes(id)
    for t in perm:
        test = str(t[len(t)-1,:])
        if dbg:
            print("test", test)
        if test == v:
            tile[id] = t
            #break
            count += 1

    if dbg:
        print("orient_tile_right", count)

def orient_tile_left(id, v):
    perm = tile_permutes(id)
    for t in perm:
        if str(t[0,:]) == str(v):
            tile[id] = t
            break

def orient_tile_top(id, v):
    perm = tile_permutes(id)
    for t in perm:
        if str(t[:,0]) == str(v):
            tile[id] = t
            break

# not using numpy block as its [row][col] and i'm currently thinking in [x][y]
def print_board():
    for ty in range(len(grid)):
    # todo: just printing top row for focus
    #for ty in range(1):
        # 10 = len(tile)
        for y in range(10):
            row = ""
            for tx in range(len(grid[ty])):
                t = tile[grid[tx][ty]]
                for x in range(len(t)):
                    if t[x][y] == 0:
                        row += '.'
                    else:
                        row += '#'
                row += '|'
            print(row)
        print("---------------------------------")

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

# top left
cur = corner_t.pop()
grid[0][0] = cur

# top edges
for x in range(1,s-1):
    neighbours = edge[cur]
    for t in neighbours:
        if t in edge_t:
            edge_t.remove(t)
            grid[x][0] = t
            break
    cur = grid[x][0]

#top right
neighbours = edge[cur]
for t in neighbours:
    if t in corner_t:
        corner_t.remove(t)
        grid[s-1][0] = t
        break

# color in left to right, always checking top
remain = corner_t | edge_t | center_t
for y in range(1,s):
    for x in range(0,s):
        top = grid[x][y-1]
        neighbours = edge[top]
        for t in neighbours:
            if t in remain:
                remain.remove(t)
                grid[x][y] = t
                break

# at this point, tiles are in the correct positions, but not oriented correctly
# use common_edge to drive orientation

# orient top left (against right column)
t1 = grid[0][0]
v = get_common_edge(t1, grid[1][0])
orient_tile_right(t1, v)
# at this point, our right edge is correct, but might need a horizontal flip
v = get_common_edge(t1, grid[0][1])
# 9 = bot row
test = str(tile[t1][:,9]) 
# [::-1] python string reverse using slicing
if not (test == v or test == v[::-1]):
    # horizontal flip needed
    tile[t1] = np.fliplr(tile[t1])

# orient top row (left neighbour on left column)
for x in range(1,s):
    neighbour = tile[grid[x-1][0]]
    v = neighbour[9,:]
    orient_tile_left(grid[x][0], v)

# orient the rest (top neighbour on top row
for y in range(1,s):
    for x in range(0,s):
        neighbour = tile[grid[x][y-1]]
        v = neighbour[:,9]
        orient_tile_top(grid[x][y], v)

print_board()
