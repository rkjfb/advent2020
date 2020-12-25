import re
import json
import copy
#import numpy as np
from collections import deque
import math

# example 1
#cardp = 5764801
#doorp = 17807724

# original
cardp = 5099500
doorp = 7648211

# returns loop for (sub,key)
def find_loop(sub, key):
    init = 1

    val = init
    loop = 0
    while not val == key:
        val *= sub
        val %= 20201227
        loop += 1

    return loop

# returns val for (sub,loop)
def find_val(sub, loop):
    init = 1
    val = init
    for i in range(loop):
        val *= sub
        val %= 20201227

    return val

sub = 7
card_loop = find_loop(sub, cardp)
print("card_loop", card_loop)

door_loop = find_loop(sub, doorp)
print("door_loop", door_loop)

door_enckey = find_val(doorp, card_loop)
print("door_enckey", door_enckey)

card_enckey = find_val(cardp, door_loop)
print("card_enckey", card_enckey)
