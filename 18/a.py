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
    #print("simple", line)
    if "(" in line or ")" in line:
        print("simpleunexpected", line)

    if "+" in line and "*" in line:
        print("simpleunexpected2", line)

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

    #print("simple", result, "=", line)
    return result

# destroy brackets
def plusfirst(line):
    result = 0

    while True:
        m = re.search("^(.* )(\d+ \+ \d+)(.*)$", line)
        if m is None:
            result = simple(line)
            break

        left = m.group(1)
        inner = m.group(2)
        right = m.group(3)

        result = simple(inner)

        if left == "" and right == "":
            break
        else:
            line = left + str(result) + right

    #print("plusfirst", result, "=", line)
    return result


# destroy brackets
def bracket(line):
    result = 0

    while True:
        m = re.search("^(.*)\(([^)]*)\)(.*)$", line)
        if m is None:
            result = plusfirst(line)
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
    print(r)
    s += r

print("sum", s)

