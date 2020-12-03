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

x = 0
y = 0
hit = 0

stride = len(slope)

while y < iny:
    t = slope[x % stride][y]
    if t == 1:
        hit = hit + 1

    x = x + 3
    y = y + 1

print(hit, " trees hit")


