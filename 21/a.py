import re
import json
import copy
#import numpy as np
from collections import deque
import math

# dict[allergen] -> set containining intersection of all lists containing allergen
allergen = dict()
all_ingredients = []

data = open("data.txt", "r")
lines = data.readlines()

for line in lines:
    if line == "\n":
        continue

    line = line.strip()

    m = re.search("^(.*) \(contains (.*)\)$", line)
    ingredients = set(m.group(1).split(" "))
    all_ingredients += ingredients
    line_allergen = m.group(2).split(",")

    for a in line_allergen:
        b = a.strip()
        if b in allergen:
            allergen[b] &= ingredients
        else:
            allergen[b] = ingredients.copy()

all_allergens = set()
for k,v in allergen.items():
    all_allergens |= v

count = 0

for i in all_ingredients:
    if not i in all_allergens:
        count += 1

size = 0
processed = set()
while True:
    # build the current list of allergens with exactly one ingredient
    one = set()
    for k,v in allergen.items():
        if k not in processed:
            if len(v) == 1:
                one.add(k)

    if len(one) == 0:
        break

    # remove the exactly one from others
    for a in one:
        ingredient = list(allergen[a])[0]
        for k,v in allergen.items():
            if not k == a and ingredient in v:
                v.remove(ingredient)

    # remember that we've processeed these allergens
    processed |= one



print(allergen)
print(all_allergens)
print(all_ingredients)
# 2078
print("count", count)

answer = ""
for k,v in sorted(allergen.items()):
    answer += list(v)[0] + ","

print("answer", answer)




