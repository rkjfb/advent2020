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

def check(l, sum):
    foundsum = False
    for x in l:
        for y in l:
            if x + y == sum:
                foundsum = True
                break
        if foundsum:
            break

    return foundsum

index = 0
value = 0

# find sequnce break
for i in range(window, len(code)):

    s = code[i-window:i]

    if not check(s, code[i]):
        print("checkfail", i, code[i])
        index = i
        value = code[i]
        break

# find contiguous sum
foundsum = False
range_start = 0
range_end = 0
for i in range(len(code)):
    sum = 0
    for j in range(i, len(code)):
        sum = sum + code[j]
        if value == sum:
            foundsum = True
            print("found sequence", i, code[i], j, code[j])
            range_start = i
            range_end = j
            break
        if sum > value:
            # gone too far
            break
    if foundsum:
        break

sublist = code[range_start:range_end]
print("code", min(sublist), max(sublist), min(sublist) + max(sublist))


