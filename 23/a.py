import re
import json
import copy
#import numpy as np
from collections import deque
import math

# cup circle
# current = [0]
cups = []
#line = "389125467"
line = "418976235"

for c in line:
    cups.append(int(c))

# removes the next 3 cups after current. current is always index 0
def remove():
    global cups
    ret = cups[1:4]
    cups = cups[0:1] + cups[4:]
    return ret

# returns the index of the destination cup
def next(v):
    v -= 1
    while not v in cups:
        v -= 1
        if v < min(cups):
            v = max(cups)

    return cups.index(v)

def round():
    global cups

    removed = remove()
    index = next(cups[0])

    # insert immediately clockwise of destination cup
    cups = cups[0:index+1] + removed + cups[index+1:]

    # current cup changed to immediate right of current cup
    cups = cups[1:] + cups[0:1]

print(cups)

for i in range(100):
    round()
    print(cups)

index_one = cups.index(1)
score = cups[index_one+1:] + cups[0:index_one]
answer = ""
for i in score:
    answer += str(i)
print(answer)
