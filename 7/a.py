import re
import json

data = open("data.txt", "r")
lines = data.readlines()

# hash[bag] = list of bags that contain it
graph = dict()

for line in lines:

    # light red bags contain 1 bright white bag, 2 muted yellow bags.
    m = re.search('^(.*) bags contain (.*)\.$', line)
    if m == None:
        print("match failed");

    dst = m.group(1)
    #print(dst)
    inner = m.group(2)

    # faded blue bags contain no other bags.
    if inner == "no other bags":
        continue

    s = inner.split(", ")
    for o in s:
        m = re.search('\d* (.*) bag', o)
        src = m.group(1)
        #print("--", src)

        if not src in graph:
            graph[src] = set()

        graph[src].add(dst)

    #s = re.split('\d* (.*) bags*, ', inner)

tovisit = graph["shiny gold"]
visited = set()

while not len(tovisit) == 0:
    nexttovisit = set()
    for v in tovisit:
        visited.add(v)

        #print(v)

        if not v in graph:
            # its possible nothing contains the bag
            continue

        for n in graph[v]:
            if not n in visited:
                nexttovisit.add(n)

    tovisit = nexttovisit

print("visited", len(visited))
