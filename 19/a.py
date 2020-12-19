import re
import json
import copy
#import numpy as np
from collections import deque
import math

class Op:
    def match(self, line):
        return 0

op = {}

class Literal:
    def __init__(self, index, lit):
        if len(lit) != 1:
            print("notlit", lit)

        self.index = index
        self.lit = lit

    # returns 0 if no match
    # returns count of characters in list line that matched
    def match(self, line):
        ret = 0
        if len(line) > 0 and line[0] == self.lit:
            ret = 1

        #print("lit" + str(self.index) + self.lit, line, ret)

        return ret

class Sequence:
    def __init__(self, index, seq):
        self.index = index
        self.seq = seq

    def match(self, line):
        pos = line
        ret = 0
        for i in self.seq:
            #print("seqmatch2", i)
            m = op[i].match(pos)
            ret += m
            if m == 0:
                # early out as sequence failed
                #print("seq" + str(self.index), pos, " - early out")
                return 0
            pos = pos[m:]

        #print("seq" + str(self.index), line, ret)

        return ret

class Or:

    # takes 2 sequences as input
    def __init__(self, index, left, right):
        self.index = index
        self.left = left
        self.right = right

    def match(self, line):
        mleft = self.left.match(line)
        mright = self.right.match(line)

        ret = max(mleft, mright)

        #print("or" + str(self.index), line, ret)

        return ret

data = open("data.txt", "r")
lines = data.readlines()

match = 0
parserules = True

def buildseq(index, line):
    s = line.split(" ")
    l = []
    for n in s:
        l.append(int(n))
    return Sequence(index, l)

for line in lines:
    if line == "\n":
        parserules = False
        continue

    line = line.strip()

    if parserules:
        s = line.split(":")
        rule = s[1].strip()
        i = int(s[0])

        if "\"" in rule:
            m = re.search("^\"(.)\"$", rule)
            if not m is None:
                op[i] = Literal(i, m.group(1))
            else:
                print("lit no match")
        elif "|" in rule:
            s2 = rule.split("|")
            seq1 = buildseq(i, s2[0].strip())
            seq2 = buildseq(i, s2[1].strip())
            op[i] = Or(i, seq1, seq2)
        else:
            op[i] = buildseq(i, rule)
    else:
        length = op[0].match(line)
        if length == len(line):
            print("match", line)
            match += 1
        else:
            print("no match", line)

print("total matches", match)



