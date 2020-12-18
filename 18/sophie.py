# copied from https://github.com/sophiebits/adventofcode/blob/main/2020/day18.py

import re
c = 0

def solve(line):
    def doInner(inner):
        print("inner", inner)
        global c
        c += 1
        return "X" + str(c)

    while '(' in line:
        def doExpr(match):
            inner = match.group(1)
            return doInner(inner)
        line = re.sub(r'\(([^()]+)\)', doExpr, line)
    return doInner(line)

s = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
print(s)
solve(s)
