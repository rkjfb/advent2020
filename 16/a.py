import re
import json
from enum import Enum
import copy
#import numpy as np
from collections import deque
import math

class Validator():
    def __init__(self, name, min1, max1, min2, max2):
        self.name = name
        self.min1 = min1
        self.max1 = max1
        self.min2 = min2
        self.max2 = max2

    def valid(self, value):
        v = False
        if self.min1 <= value <= self.max1:
            v = True
        if self.min2 <= value <= self.max2:
            v = True

        # print("valid", v, self.name, value, self.min2, self.max2)

        return v

def get_values(line):
    sp = line.split(",")
    v = []
    for s in sp:
        v.append(int(s))
    return v

rules = []
data = open("data.txt", "r")
lines = data.readlines()

# 0 = rules, 1 = your ticket, 2 = nearby
state = 0
error = 0


for line in lines:
    if line == "\n":
        continue

    if state == 2:
        if "," in line:
            values = get_values(line)
            for v in values:
                valid = False
                for r in rules:
                    if r.valid(v):
                        valid = True
                        break

                if not valid:
                    #print("invalid", v)
                    error += v

    if state == 1:
        if "," in line:
            values = get_values(line)
        else:
            if "nearby tickets" in line:
                state = 2
            else:
                print("confused2:", line)

    if state == 0:
        m = re.search("(.*): (\d*)-(\d*) or (\d*)-(\d*)", line)
        if not m is None:
            rules.append(Validator(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))))
        else:
            if "your ticket" in line:
                state = 1
            else:
                print("confused 1", line)

#part 1: 18227
print("error", error)
