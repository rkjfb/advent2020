import re
import json
import copy
import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

tile = dict()
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


print(tile[3079])


