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
start = 0
end = code[-1] + 3

# returns true if supplied list is valid
def valid(l):
    last = 0
    for i in range(0, len(l)):
        diff = l[i] - last

        if diff > 3:
            return False

        last = l[i]

    if end - l[-1] > 3:
        return False

    return True

# returns count of legal permutations of l
def permute(l, start):

    if not valid(l):
        return 0

    # we're valid
    total = 1

    for i in range(start, len(l)):
        new_list = l.copy()
        new_list.remove(l[i])

        total += permute(new_list, i)

    return total

print(permute(code, 0))


