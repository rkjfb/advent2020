import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

# no brackets eval
def simple(line):
    #print(line)
    if "(" in line or ")" in line:
        print("simpleunexpected", line)

    result = 0

    while True:
        m = re.search("^(\d+) (.) (\d+)(.*)$", line)
        if m is None:
            m2 = re.search("^(\d)$", line)
            if m2 is None:
                print("simplenomatch", line)
            else:
                result = int(m2.group(1))
                break

        left = int(m.group(1))
        op = m.group(2)
        right = int(m.group(3))
        extra = m.group(4)

        if op == '+':
            result = left + right
        elif op == '*':
            result = left * right

        if extra == "":
            break
        else:
            line = str(result) + extra

    return result

# destroy brackets
def bracket(line):
    result = 0

    while True:
        m = re.search("^(.*)\(([^)]*)\)(.*)$", line)
        if m is None:
            result = simple(line)
            break

        left = m.group(1)
        inner = m.group(2)
        right = m.group(3)

        result = bracket(inner)

        if left == "" and right == "":
            break
        else:
            line = left + str(result) + right

    return result

s = 0
for line in lines:
    if line == "\n":
        continue
    r = bracket(line)
    s += r

print("sum", s)

