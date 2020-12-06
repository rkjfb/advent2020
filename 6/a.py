import re
import json

data = open("data.txt", "r")
lines = data.readlines()

valid = 0

choice = set()
newbatch = True

for line in lines:
    if line == "\n":
        valid = valid + len(choice)
        #print(choice)
        choice = set()
        newbatch = True
        continue

    person = set()
    for x in line:
        if x =='\n':
            continue

        person.add(x)

    if newbatch:
        choice = person
    else:
        choice = choice.intersection(person)

    newbatch = False

print("valid", valid)


