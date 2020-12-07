import re
import json

data = open("data.txt", "r")
lines = data.readlines()

# hash[bag] = (hash[bag] = count)
# light red bags contain 1 bright white bag, 2 muted yellow bags.
# graph[light red] = { "bright white" : 1, "muted yellow" : 2 }
graph = dict()

for line in lines:

    # light red bags contain 1 bright white bag, 2 muted yellow bags.
    m = re.search('^(.*) bags contain (.*)\.$', line)
    if m == None:
        print("match failed");

    main = m.group(1)
    #print(dst)
    inner = m.group(2)

    # faded blue bags contain no other bags.
    if inner == "no other bags":
        continue

    s = inner.split(", ")
    for o in s:
        m = re.search('(\d*) (.*) bag', o)
        count = m.group(1)
        inside = m.group(2)
        #print("--", src)

        if not main in graph:
            graph[main] = dict()

        graph[main][inside] = count

    #s = re.split('\d* (.*) bags*, ', inner)

#print(graph)

tovisit = "shiny gold"

def rec(color):
    count = 1
    if color in graph:
        for key, value in graph[color].items():
            count = count + int(value) * rec(key)

    return count

print(tovisit, rec(tovisit) - 1)
