import re
import json
from enum import Enum
import copy

class Seat(Enum):
    FLOOR = 0
    EMPTY = 1
    OCCUPIED = 2

data = open("data.txt", "r")
lines = data.readlines()

# list of numbers
seat = list()
first = True

for line in lines:
    x = 0
    for c in line:
        if c == '\n':
            continue

        if first:
            seat.append([])

        if c == '.':
            seat[x].append(Seat.FLOOR)
        elif c == 'L':
            seat[x].append(Seat.EMPTY)
        elif c == '#':
            seat[x].append(Seat.OCCUPIED)
        else:
            print("what", c)

        x += 1

    first = False

def printseat(s):
    for j in range(len(s[0])):
        line = ""
        for i in range(len(s)):
            if s[i][j] == Seat.FLOOR:
                line += "."
            elif s[i][j] == Seat.EMPTY:
                line += "L"
            else:
                line += "#"

        print(line)

# returns the number of occupied seats around s
def occupied(s, i, j):
    startx = max(0, i-1);
    endx = min(len(s)-1, i+1)
    starty = max(0, j-1);
    endy = min(len(s[i])-1, i+1)

    count = 0

    for x in range(startx, endx, 1):
        for y in range(starty, endy, 1):
            if not (x == i and y == j):
                if s[i][j] == Seat.OCCUPIED:
                    count += 1

    return count

# returns a new state of seats
def update(s):
    n = copy.deepcopy(s)

    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] == Seat.EMPTY and occupied(s, i, j) == 0:
                n[i][j] = Seat.OCCUPIED
            if s[i][j] == Seat.OCCUPIED and occupied(s, i, j) >= 4:
                n[i][j] = Seat.EMPTY

    return n

printseat(seat)
print("|||")

a = update(seat)
printseat(a)
print("|||")

b = update(a)
printseat(b)
print("|||")
