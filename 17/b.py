import re
import json
from enum import Enum
import copy
#import numpy as np
from collections import deque
import math

# dict[tuple(x,y,z)] = 0|1
world = {}

start = [0,0,0,0]
end = [2,2,0,0]
search = 1

def get_world(world,x,y,z,w):
    key = x,y,z,w
    if key in world:
        return world[key]
    return 0

# neighbour count in world at (ox,oy,oz,ow)
def count_world(world, ox, oy, oz, ow):
    count = 0

    for x in range(ox-1,ox+2,1):
        for y in range(oy-1,oy+2,1):
            for z in range(oz-1,oz+2,1):
                for w in range(ow-1,ow+2,1):
                    if x == ox and y == oy and z == oz and w == ow:
                        continue
                    if get_world(world,x,y,z,w) == 1:
                        count += 1

    return count


def step():
    global world
    n = world.copy()

    global search

    for x in range(start[0]-search, end[0]+search+1):
        for y in range(start[1]-search, end[1]+search+1):
            for z in range(start[2]-search, end[2]+search+1):
                for w in range(start[3]-search, end[3]+search+1):

                    dbg = False
                    if x == 1111 and y == 0 and z == 0:
                        dbg = True

                    count = count_world(world, x, y, z, w)

                    if dbg:
                        print("dbgcount", x, y, z, w, "=", count)

                    v = get_world(world, x, y, z, w)

                    if v == 1:
                        if not (count == 2 or count == 3):
                            n[x,y,z,w] = 0

                    if v == 0 and count == 3:
                        n[x,y,z,w] = 1

    world = n

    # each time the world grows, we need to search 1 step wider
    search += 1

def printworld():
    print("topleft", start[0]-search, start[1]-search)
    for y in range(start[1]-search, end[1]+search+1):
        line = ""
        for x in range(start[0]-search, end[0]+search+1):
            if get_world(world,x,y,0,0) == 0:
                line += "."
            else:
                line += "#"
        print(line)

def printcount():
    count = 0
    for v in world.values():
        if v == 1:
            count += 1
    print("count", count)

data = open("data.txt", "r")
lines = data.readlines()

y = 0
for line in lines:
    x = 0
    for c in line:
        if c == '.':
            world[x,y,0,0] = 0
        elif c == '#':
            world[x,y,0,0] = 1
        elif c == '\n':
            continue
        else:
            print("confused: ", c)
        x += 1
    y += 1

end = [x,y,0,0]

print("init")
printworld()

for i in range(6):
    step()
    print()
    print(" ** ", i, " ** ")
    printworld()
    # wrong: 152
    printcount()

