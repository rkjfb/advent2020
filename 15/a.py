import re
import json
from enum import Enum
import copy
#import numpy as np
from collections import deque
import math

class NumberData:
    def __init__(self, t):
        self.turn = t
        self.lastturn = 0

    def addturn(self, t):
        self.lastturn = self.turn
        self.turn = t

# puzzle data

# 436
# 175594
#data = [0,3,6] 

# 1
#data = [1,3,2]

data = [13,0,10,12,1,5,8]

# map: value -> turn last spoken
spoken = dict()

# populate starting numbers
turn = 1
last = 0
for d in data:
    spoken[d] = NumberData(turn)
    last = d
    turn += 1

for t in range(turn, 30000001, 1):
    # last must exist
    say = spoken[last].lastturn
    if say != 0:
        say = spoken[last].turn - spoken[last].lastturn

    if say in spoken:
        spoken[say].addturn(t)
    else:
        spoken[say] = NumberData(t)

    #print("turn", t, "say", say)

    last = say

print(last)

