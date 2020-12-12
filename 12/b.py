import re
import json
from enum import Enum
import copy
import numpy as np
from collections import deque

north = np.array([0, 1])
east = np.array([1, 0])
south = np.array([0, -1])
west = np.array([-1, 0])

#shipdir = deque([east, south, west, north])
shippos = np.array([0,0])
way = np.array([10,1])

data = open("data.txt", "r")
lines = data.readlines()

# single rotate 90 clockwise around origin
def rot90(v):
    return np.array([v[1], -v[0]])

def rotate(rot):
    rot = rot % 4

    global way

    for i in range(rot):
        way = rot90(way)


for line in lines:
    m = re.search("^(.)(\d+)$", line)
    instr = m.group(1)
    num = int(m.group(2))

    print("ship", shippos, "way", way)

    if instr=="N":
        way += num * north
    elif instr=="S":
        way += num * south
    elif instr=="W":
        way += num * west
    elif instr=="E":
        way += num * east
    elif instr=="F":
        delta = num * way
        shippos += delta
    elif instr=="R":
        rotate(int(num/90))
    elif instr=="L":
        rotate(int(num/-90))
    else:
        print("what", instr)

print("shippos", shippos, abs(shippos[0]) + abs(shippos[1]))
