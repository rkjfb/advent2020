import re
import json
import copy
#import numpy as np
from collections import deque
import math
#import cProfile, pstats, io
import time

# input data
#line = "389125467"
line = "418976235"
#line = "123456789"
print("input", line)

# build input
full_input = []
for c in line:
    full_input.append(int(c))
for i in range(max(full_input)+1, 1000001):
#for i in range(max(full_input)+1, 21):
    full_input.append(i)

# cup circle
# singly-linked circular list implemented inside a list
# index = node identity
# value = next pointer
# +1 index==node value property
nextcup = [-1] * (len(full_input)+1)
prevcup = [-1] * (len(full_input)+1)
head = -1


# build initial list based on input
last = -1
for c in full_input:
    val = c
    if not last == -1:
        nextcup[last] = val
        prevcup[val] = last
    else:
        head = val
    last = val
nextcup[last] = head
prevcup[head] = last

gmax = max(nextcup)

print("expect1000001", len(nextcup))

def popleft():
    global head, nextcup, prevcup

    ret = head
    prev_index = prevcup[head]
    next_index = nextcup[head]

    nextcup[prev_index] = next_index
    prevcup[next_index] = prev_index

    nextcup[head] = -1
    prevcup[head] = -1

    head = next_index

    return ret

def appendleft(val):
    global head, nextcup, prevcup

    prev_index = prevcup[head]

    nextcup[val] = head
    prevcup[head] = val

    nextcup[prev_index] = val
    prevcup[val] = prev_index

    head = val

def print_list():
    global head, nextcup, prevcup
    line = ""
    cur = head
    line = str(cur)
    cur = nextcup[cur]
    while not cur == head:
        line += str(cur)
        cur = nextcup[cur]

    print("head", head, line)

# removes the next 3 cups after current. current is always left most
def remove():
    head = popleft()
    ret = []
    ret.append(popleft())
    ret.append(popleft())
    ret.append(popleft())
    appendleft(head)
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
    v = dec_v(v)

    while nextcup[v] == -1:
        v = dec_v(v)

    return v

def round():
    global head

    removed = remove()
    next_head = nextcup[head]

    # insert immediately clockwise of destination cup
    head = nextcup[next(head)]
    appendleft(removed[2])
    appendleft(removed[1])
    appendleft(removed[0])

    # current cup changed to immediate right of current cup
    head = next_head

start = time.time()
last = start

for i in range(10000000):
    if i % 10000 == 0:
        t = time.time()
        if t - last > 1:
            print(t - start, "round", i)
            last = t
    round()

v1 = nextcup[1]
v2 = nextcup[v1]
print("answer", v1,v2,v1*v2)
