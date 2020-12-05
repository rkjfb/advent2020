import re
import json

data = open("data.txt", "r")
lines = data.readlines()

valid = 0
maxseat = 0
found = set()

for line in lines:
    line = line.replace("F", "0")
    line = line.replace("B", "1")
    line = line.replace("L", "0")
    line = line.replace("R", "1")

    m = re.search('^(.{7})(.{3})$', line)
    if m == None:
        print("match failed");

    row = int(m.group(1), 2)
    col = int(m.group(2), 2)
    id = row * 8 + col

    found.add(id)

for i in range(1024):
    if not i in found:
        print(i)



