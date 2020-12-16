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
        self.maybe = []
        self.index = -1

    def valid(self, value):
        v = False
        if self.min1 <= value <= self.max1:
            v = True
        if self.min2 <= value <= self.max2:
            v = True

        #print("valid", v, self.name, value)

        return v

    # adds a candidate index
    def add_maybe(self, i):
        self.maybe.append(i)

    # if there is exactly one maybe takes that index and returns it
    # returns -1 if couldn't close
    # returns -2 if already closed
    def close_maybe(self):
        if not self.index == -1:
            # if we've already closed, fail
            return -1

        if len(self.maybe) == 1:
            self.index = self.maybe[0]

        # clear maybe list to cycle can happen again
        self.maybe = []

        return self.index

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

myticket = []
nearby = []

for line in lines:
    if line == "\n":
        continue

    if state == 2:
        if "," in line:
            values = get_values(line)
            valid = True
            for v in values:
                fieldvalid = False
                for r in rules:
                    if r.valid(v):
                        fieldvalid = True
                        break

                if not fieldvalid:
                    valid = False

            if valid:
                nearby.append(values)

    if state == 1:
        if "," in line:
            myticket = get_values(line)
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

# indices currently up for grabs
avail = set()
for i in range(len(myticket)):
    avail.add(i)

for loop in range(len(rules)):
    for r in rules:
        for i in avail:
            allvalid = True
            for n in nearby:
                #print("nearbyloop", n[i])
                if not r.valid(n[i]):
                    #print("invalid", r.name, n)
                    allvalid = False
                    break
            if allvalid:
                r.add_maybe(i)

    for r in rules:
        i = r.close_maybe()
        if not i == -1:
            avail.remove(i)

    print(loop, avail)

    if not avail:
        break

product = 1
for r in rules:
    if "departure" in r.name:
        product *= myticket[r.index]

# 2355350878831
print("product", product)
        

