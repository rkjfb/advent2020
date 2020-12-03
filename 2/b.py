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

    count = 0
    if match[mmin-1] == char:
        count = count + 1
    if match[mmax-1] == char:
        count = count + 1

    if count == 1:
        valid = valid + 1

print("total valid", valid)
