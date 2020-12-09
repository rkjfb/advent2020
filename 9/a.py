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

print(len(code))
print("hello")

for i in range(window, len(code)):

    s = code[i-window:i]

    if not check(s, code[i]):
        print("checkfail", i, code[i])
        break

