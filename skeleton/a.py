import re
import json
import copy
#import numpy as np
from collections import deque
import math

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

answer = ""

print("answer", answer)




