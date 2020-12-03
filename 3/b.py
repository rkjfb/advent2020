import re

data = open("data.txt", "r")
lines = data.readlines()
valid = 0

slope = []
iny = 0
for line in lines:
    x = 0
    for char in line:
        if char == '\n':
            continue

        if iny == 0:
            slope.append([])

        if char == '.':
            slope[x].append(0)
        else:
            slope[x].append(1)
        x = x + 1
    iny = iny + 1

inslopes = [[1,1],[3,1],[5,1],[7,1],[1,2]]

stride = len(slope)
product = 1

for inslope in inslopes:
    x = 0
    y = 0
    hit = 0

    while y < iny:
        t = slope[x % stride][y]
        if t == 1:
            hit = hit + 1

        x = x + inslope[0]
        y = y + inslope[1]

    product = product * hit

print(product, " tree hit product")


