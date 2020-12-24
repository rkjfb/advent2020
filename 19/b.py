import re
import json
import copy
#import numpy as np
from collections import deque
import math

# todo: learn more about logging.debug, briefly tried and it was dumping call stacks
debug = False

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

    # returns a list of matches
    # list is empty if no match occured
    def match(self, line):
        ret = [] 
        if len(line) > 0 and line[0] == self.lit:
            ret = [1]

        if debug:
            print("lit" + str(self.index) + self.lit, line, ret)

        return ret

class Sequence:
    def __init__(self, index, seq):
        self.index = index
        self.seq = seq

    def match(self, line):
        # using sets as we're just measuring distance into line
        # if there are two ways to get the same distance, it's still match
        inputs = set()
        inputs.add(0)
        outputs = set()

        for step in self.seq:

            outputs = set()
            for i in inputs:
                matches = op[step].match(line[i:])
                for o in matches:
                    if o == 0:
                        continue
                    # we can now match (o+i) into line
                    outputs.add(o + i)

            if len(outputs) == 0:
                # early out as sequence failed
                if debug:
                    print("seq" + str(self.index), line, " - early out")
                return []
            
            inputs = outputs

        ret = list(outputs)
        if debug:
            print("seq" + str(self.index), line, ret)

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

        merge = mleft + mright

        if 0 in merge:
            merge.remove(0)

        if debug:
            print("or" + str(self.index), line, merge)

        return merge

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
        matches = op[0].match(line)
        if len(line) in matches:
            print("match", line)
            match += 1
        else:
            print("no match", line)

print("total matches", match)



