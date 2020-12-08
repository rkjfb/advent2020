import re
import json

accumulator = 0
instruction = 0

#TODO: learn python abc class inherit
class Nop:
    def __init__(self):
        self.visited = False

    def run(self):
        if self.visited:
            return False

        global instruction
        instruction = instruction + 1

        self.visited = True
        return True

class Accumulate:
    def __init__(self, val):
        self.val = val
        self.visited = False

    def run(self):
        if self.visited:
            return False

        global accumulator 
        global instruction

        accumulator = accumulator + self.val
        instruction = instruction + 1
        self.visited = True
        return True

class Jump:
    def __init__(self, skip):
        self.skip = skip
        self.visited = False

    def run(self):
        if self.visited:
            return False

        global instruction

        instruction = instruction + self.skip
        self.visited = True
        return True

data = open("data.txt", "r")
lines = data.readlines()

# list of instructions
program = list()

for line in lines:

    # nop +0
    # acc +1
    # jmp +4
    # acc +3
    m = re.search('^(...) (.*)$', line)
    if m == None:
        print("match failed");

    op = m.group(1)
    val = int(m.group(2))
    instr = None

    if op == "nop":
        instr = Nop()
    elif op == "acc":
        instr = Accumulate(val)
    elif op == "jmp":
        instr = Jump(val)
    else:
        print("unrecognized op")

    program.append(instr)

print(len(program))
while True:
    ret = program[instruction].run()
    #print("instruction", instruction, "ret", ret)
    if not ret:
        break

print("accumulator", accumulator)
