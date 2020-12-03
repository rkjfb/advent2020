import re

data = open("data.txt", "r")
lines = data.readlines()
valid = 0

for line in lines:
    m = re.search('(\d+)-(\d+) (.): (.*)', line)
    mmin = int(m.group(1))
    mmax = int(m.group(2))
    char = m.group(3)
    match = m.group(4)
    count = match.count(char)
    #print(mmin, mmax, count)
    if count >= mmin and count <= mmax:
        valid = valid + 1

print("total valid", valid)
