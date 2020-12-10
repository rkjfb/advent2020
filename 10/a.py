import re
import json

window = 25

data = open("data.txt", "r")
lines = data.readlines()

# list of numbers
code = list()

for line in lines:
    val = int(line)
    code.append(val)

code.sort()
code.append(code[len(code) - 1]+3)

print(code)

last = 0
d1 = 0
d3 = 0
for i in range(0, len(code)):

    diff = code[i] - last
    print(last, code[i], diff)
    if diff == 1:
        d1 += 1
    if diff == 3:
        d3 += 1

    last = code[i]

print("d1", d1, "d3", d3, d1 * d3)


