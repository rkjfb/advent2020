import re
import json
from enum import Enum
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

ormask = 0
andmask = 0
mem = {}

def setmask(special):
    nox = special.replace('X', '0')
    global ormask
    ormask = int(nox, 2)
    nox2 = special.replace('X', '1')
    global andmask
    andmask = int(nox2, 2)

def setmem(index, value):
    mem[index] = value
    mem[index] &= andmask
    mem[index] |= ormask

for line in lines:
    remask = re.search("mask = (.*)", line)
    remem = re.search("mem\[(\d+)\] = (\d+)", line)
    if not remask is None:
        setmask(remask.group(1))
    elif not remem is None:
        setmem(int(remem.group(1)), int(remem.group(2)))
    else:
        print("what?", line)

print("sum", sum(mem.values()))
