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
        # order modulus bus time, as we're only looking up to bus time ahead
        # this is fine cause if bus+o is good, then bus + o + n * t is good
        bus.append(BusData(int(t), order%int(t)))
    order += 1

# start with the biggest bus time
search = bus.copy()
search.sort(key=operator.attrgetter('time'))
search.reverse()

print(search)

busmax = search[0]
search.remove(busmax)

cur = busmax.time - busmax.offset
step = busmax.time

for bus in search:
    while True:
        # check current
        next_t = bus.time * math.ceil(cur/bus.time)
        if next_t == cur + bus.offset:
            break

        cur += step

    # at this point we know the buses so far all align, therefore we can step by their product
    step *= bus.time

print(cur)
