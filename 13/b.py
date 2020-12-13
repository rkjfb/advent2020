#import re
#import json
#from enum import Enum
#import copy
#import numpy as np
#from collections import deque
import math
import operator

data = open("data.txt", "r")
lines = data.readlines()

# don't think my python has dataclass
class BusData:
    def __init__(self, t, o):
        # bus id 
        self.time = t
        # bus offset from 0
        self.offset = o

    def __repr__(self):
        return str(self.time) + "@" + str(self.offset)

bus = []

s = lines[1].split(",")
order = 0
for t in s:
    if not t == "x":
        bus.append(BusData(int(t), order))
    order += 1

# start with the biggest bus time
search = bus.copy()
search.sort(key=operator.attrgetter('time'))
search.reverse()

print(search)

busmax = search[0]
search.remove(busmax)

# where we start searching
cur = busmax.time - busmax.offset
found = False

while True:
    # check current
    found = True
    for b in search:
        next_t = b.time * math.ceil(cur/b.time)
        if not next_t == cur + b.offset:
            found = False
            break

    if found:
        break

    cur += busmax.time

print(cur)
