import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

player = 0 
deck = [deque()]

for line in lines:
    if line == "\n":
        continue

    line = line.strip()

    if "Player" in line:
        if len(deck[player]) > 0:
            player += 1
            deck.append(deque())

        if player == 2:
            break
        continue

    deck[player].append(int(line))

def round():
    first = deck[0].popleft()
    second = deck[1].popleft()
    if (first > second):
        deck[0].append(first)
        deck[0].append(second)
    else:
        deck[1].append(second)
        deck[1].append(first)

def score():
    p = deck[0]
    if len(p) == 0:
        p = deck[1]

    score = 0

    while len(p) > 0:
        m = len(p)
        score += p.popleft() * m
        #print(score)

    print("score", score)

count = 1

while len(deck[0]) > 0 and len(deck[1]) > 0:
    round()
    #print(count, deck)
    count += 1

    if count > 9999:
        print("failed to complete")
        break

score()

