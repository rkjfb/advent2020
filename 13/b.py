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
        bus.append(BusData(int(t), order%int(t)))
    order += 1

# start with the biggest bus time
search = bus.copy()
search.sort(key=operator.attrgetter('time'))
search.reverse()

print(search)

busmax = search[0]
search.remove(busmax)


# where we start searching
# search for 2nd biggest
cur = busmax.time - busmax.offset
bus2 = search[0]
step = busmax.time

while True:
    # check current
    next_t = bus2.time * math.ceil(cur/bus2.time)
    if next_t == cur + bus2.offset:
        break

    cur += step

# at this point we know the first place where #1 and #2 align, there we can step by their product
step = busmax.time * bus2.time
search.remove(bus2)

# does this extend to 3 buses?
bus3 = search[0]

while True:
    # check current
    next_t = bus3.time * math.ceil(cur/bus3.time)
    if next_t == cur + bus3.offset:
        print("found bus3!")
        break

    cur += step

step *= bus3.time
search.remove(bus3)

# does this extend to 4 buses?
bus4 = search[0]

while True:
    # check current
    next_t = bus4.time * math.ceil(cur/bus4.time)
    if next_t == cur + bus4.offset:
        print("found bus4!")
        break

    cur += step

step *= bus4.time
search.remove(bus4)

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

    cur += step

print(cur)
