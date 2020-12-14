import re
import json
from enum import Enum
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

# bits to float on
masklist = []

# mem address should be or'd with this
ormask = 0

mem = {}

def setmask(special):
    nox = special.replace('X', '0')
    global ormask
    ormask = int(nox, 2)

    global masklist
    masklist = []
    speciallist = list(special)
    speciallist.reverse()
    for i,c in enumerate(speciallist):
        if c == 'X':
            masklist.append(i)

# clear bit in value
def clearbit(value, bit):
    mask = ~(1 << bit)
    return value & mask

# set bit in value
def setbit(value, bit):
    mask = 1 << bit
    return value | mask

def setmem(addr, value):
    # mask 1s overwrite address bits with 1
    addr |= ormask

    count = len(masklist)
    for r in range(2 ** count):
        newaddr = addr | ormask

        # i is the bit in r that we are reading
        # shift is the bit in newaddr that we are writing
        for i,shift in enumerate(masklist):
            if (r & 1 << i) == 0:
                newaddr = clearbit(newaddr, shift)
            else:
                newaddr = setbit(newaddr, shift)

        mem[newaddr] = value

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
