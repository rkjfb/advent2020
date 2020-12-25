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

# merge of all tiles
mega = None

# monster obliterated
megastat = None

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

def print_grid():
    for y in range(len(grid[0])):
        row = ""
        for x in range(len(grid)):
            row += str(grid[x][y]) + " "
        print(row)

# not using numpy block as its [row][col] and i'm currently thinking in [x][y]
def print_board():
    # BUGBUG for ty in range(len(grid)):
    for ty in range(3):
    # todo: just printing top row for focus
    #for ty in range(1):
        # 10 = len(tile)
        for y in range(10):
            row = ""
            # BUGBUG for tx in range(len(grid[ty])):
            for tx in range(3):
                t = tile[grid[tx][ty]]
                for x in range(len(t)):
                    if t[x][y] == 0:
                        row += '.'
                    else:
                        row += '#'
                row += '|'
            print(row)
        print("---------------------------------")

def print_mega_board():
    for y in range(len(mega[0])):
        row = ""
        for x in range(len(mega)):
            if mega[x][y] == 0:
                row += '.'
            else:
                row += '#'
        print(row)

# builds mega board
# technically, flipped, but doesn't matter for our purposes
def build_mega():
    global mega
    mega = []
    for ty in range(len(grid)):
        # 10 = len(tile)
        # BUGBUG:skip last row, except for last tile
        range_y = 9
        if ty == len(grid)-1:
            range_y = 10
        for y in range(1,9):
            row = []
            line = ""
            for tx in range(len(grid[ty])):
                t = tile[grid[tx][ty]]

                # BUGBUG:skip last column, except for last tile
                range_x = len(t)-1
                if tx == len(grid[ty])-1:
                    range_x += 1

                for x in range(1,9):
                    row.append(t[x][y])
                    if t[x][y] == 0:
                        line += '.'
                    else:
                        line += '#'
            mega.append(row)
            #print(line)

# builds monster from problem string input
def build_monster():
    m = []

    # baby monster that is definitely at (0,0) - so we should find it.
    #m.append("#   ##")
    #m.append("  # # ")

    # rotated baby monster at (0,0)
    #m.append("  ####")
    #m.append("#  #  ")

    m.append("                  # ")
    m.append("#    ##    ##    ###")
    m.append(" #  #  #  #  #  #   ")

    row = []
    for line in m:
        d = []
        for c in line:
            if c == '#':
                d.append(1)
            else:
                d.append(0)
        row.append(d)
    
    global monster
    monster = np.array(row)

# returns list of all monster permutations
def monster_permutes():
    ret = []
    m = monster
    for i in range(4):
        m = np.rot90(m)
        ret.append(m)
    m = np.fliplr(monster)
    for i in range(4):
        m = np.rot90(m)
        ret.append(m)
    return ret

# clears monster m bits at (x,y) in megastat
def clear_monster(m, sx, sy):
    global megastat
    for x in range(len(m)):
        for y in range(len(m[0])):
            if m[x][y] == 1:
                megastat[sx+x][sy+y] = 0


# find monster m in mega
# there is probably some numpy shortcut here involving masks
def find_monster(m):
    search_x = len(mega) - len(m) + 1
    search_y = len(mega[0]) - len(m[0]) + 1
    #search_x = 1
    #search_y = 1

    for sx in range(search_x):
        for sy in range(search_y):
            found = True
            for x in range(len(m)):
                for y in range(len(m[0])):
                    if m[x][y] == 1:
                        if not mega[sx+x][sy+y] == 1:
                            found = False
            if found:
                print("found", sx, sy)
                clear_monster(m, sx, sy)

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

build_mega()
megastat = mega.copy()
build_monster()
#print_mega_board()
#print_board()
#print_grid()
print(monster)
#find_monster(monster)
monster_list = monster_permutes()
for m in monster_list:
    find_monster(m)

count = 0
for a in megastat:
    for b in a:
        if b == 1:
            count += 1

print("roughness", count)
