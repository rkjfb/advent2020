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

# returns true if ray(sx,sy,dx,dy) hits an occupied chair
def hitray(s, sx, sy, dx, dy):
    if dx == 0 and dy == 0:
        return False

    x = sx
    y = sy

    while True:
        x += dx
        y += dy

        if x < 0 or x >= len(s):
            return False

        if y < 0 or y >= len(s[0]):
            return False

        if s[x][y] == Seat.OCCUPIED:
            return True

        if s[x][y] == Seat.EMPTY:
            return False

# returns the number of occupied seats around s
def occupied(s, i, j):
    startx = max(0, i-1);
    endx = min(len(s), i+2)
    starty = max(0, j-1);
    endy = min(len(s[i]), j+2)

    count = 0

    for x in range(startx, endx, 1):
        for y in range(starty, endy, 1):
            if hitray(s, i, j, x-i, y-j):
                count += 1

    return count

# returns a new state of seats
def update(s):
    n = copy.deepcopy(s)

    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] == Seat.EMPTY and occupied(s, i, j) == 0:
                n[i][j] = Seat.OCCUPIED
            if s[i][j] == Seat.OCCUPIED and occupied(s, i, j) >= 5:
                n[i][j] = Seat.EMPTY

    return n

def countseats(s):
    count = 0
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] == Seat.OCCUPIED:
                count += 1

    return count

for i in range(1000):
    #printseat(seat)
    last = seat
    seat = update(seat)

    if seat == last:
        print("stable at iteration", i)
        print("occupied seats", countseats(seat))
        break

