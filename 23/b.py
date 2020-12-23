import re
import json
import copy
#import numpy as np
from collections import deque
import math
#import cProfile, pstats, io
import time

# cup circle
# current = [0]
cups = deque()
line = "389125467"
#line = "418976235"
#line = "123456789"

for c in line:
    cups.append(int(c))

#for i in range(max(cups)+1, 1000001):
#for i in range(max(cups)+1, 101):
#    cups.append(i)

gmax = max(cups)

print("expect1m", len(cups))

# removes the next 3 cups after current. current is always left most
def remove():
    global cups
    head = cups.popleft()
    ret = []
    ret.append(cups.popleft())
    ret.append(cups.popleft())
    ret.append(cups.popleft())
    cups.appendleft(head)
    return ret

def dec_v(v):
    if v == 1:
        v = gmax
    else:
        v -= 1
    return v

last_index = 0

# returns the index of the destination cup
def next(v):
    ret = -1
    v = dec_v(v)

    global last_index

    if cups[last_index-1] == v:
        ret = last_index - 1

    if ret == -1:
        try:
            ret = cups.index(v,last_index-10,last_index)
        except ValueError as e:
            pass

    if ret == -1:
        while True:
            try:
                ret = cups.index(v)
            except ValueError as e:
                v = dec_v(v)

            if not ret == -1:
                break

    last_index = ret
    return ret

def round():
    global cups

    removed = remove()
    index = next(cups[0])

    # insert immediately clockwise of destination cup
    cups.rotate(-index-1)
    cups.appendleft(removed[2])
    cups.appendleft(removed[1])
    cups.appendleft(removed[0])
    cups.rotate(index)

    # current cup changed to immediate right of current cup

#pr = cProfile.Profile()
#pr.enable()

start = time.time()
last = start

#for i in range(10000000):
for i in range(10):
    if i % 1000 == 0:
        t = time.time()
        if t - last > 1:
            print(t - start, "round", i)
            last = t
    round()
    print(cups)

#pr.disable()
#s = io.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print(s.getvalue())


index = cups.index(1)
cups.rotate(-index-1)
v1 = cups.popleft()
v2 = cups.popleft()
print("answer", v1,v2,v1*v2)
