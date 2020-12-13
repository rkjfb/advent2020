import re
import json
from enum import Enum
import copy
import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

avail = int(lines[0])
times = []

s = lines[1].split(",")
for t in s:
    if t == "x":
        continue

    times.append(int(t))

start = []
for t in times:
    start.append(t * math.ceil(avail / t))

nextstart = min(start)
bus = times[start.index(nextstart)]
delay = nextstart - avail

print(avail)
print(times)
print(start)
print(delay, bus, delay * bus)
