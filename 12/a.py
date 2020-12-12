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

shipdir = deque([east, south, west, north])
shippos = np.array([0,0])


data = open("data.txt", "r")
lines = data.readlines()


for line in lines:
    m = re.search("^(.)(\d+)$", line)
    instr = m.group(1)
    num = int(m.group(2))

    print("shippos", shippos, shippos[0] + shippos[1])

    if instr=="N":
        shippos += num * north
    elif instr=="S":
        shippos += num * south
    elif instr=="W":
        shippos += num * west 
    elif instr=="E":
        shippos += num * east
    elif instr=="F":
        shippos += num * shipdir[0]
    elif instr=="R":
        shipdir.rotate(int(num / -90))
    elif instr=="L":
        shipdir.rotate(int(num / 90))
    else:
        print("what", instr)

print("shippos", shippos, abs(shippos[0]) + abs(shippos[1]))
