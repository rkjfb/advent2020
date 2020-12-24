import collections
import re

l = [1,2]
s = str(l)
ll = list(s)
for i in ll:
    print(i)


t = (1,2)
d = dict()
d[t] = True
for k in d:
    i,j = k
    print(i, j)

m = re.findall('e|se|sw|w|nw|ne', "nwawasw")
for s in m:
    print(s)

d3 = collections.defaultdict(bool)
print(d3.get(2,False))
print(d3.get(3,True))

d3[2] = True
d3[7] = True

print(sum(1 for k, v in d3.items() if v))

