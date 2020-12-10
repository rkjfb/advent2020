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

code.append(0)
code.sort()
end = code[-1] + 3
code.append(end)

# hash(key) = values
value = dict()
value[end] = 1

#print(code)

length = len(code)
last = end
for i in reversed(range(length-1)):

    sum = 0;
    if i + 1 < length and code[i+1] - code[i] <= 3:
        sum += value[code[i+1]];
    if i + 2 < length and code[i+2] - code[i] <= 3:
        sum += value[code[i+2]];
    if i + 3 < length and code[i+3] - code[i] <= 3:
        sum += value[code[i+3]];

    #print(i, code[i], sum)

    value[code[i]] = sum

print(value[0]);


