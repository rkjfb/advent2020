import re
import json

class Processor:
    def __init__(self, p):
        self.accumulator = 0
        self.instruction = 0
        self.program = p

    # Returns true if program completes execution
    def execute(self):
        length = len(self.program)
        while not self.instruction == length:
            ret = self.program[self.instruction].run(self)
            if not ret:
                break

        if self.instruction == length:
            return True

        return False

class Instruction:
    def __init__(self, data):
        # data is not used by Instruction, though common to children
        self.data = data
        self.visited = False

    def run(self, proc):
        if self.visited:
            return False

        proc.instruction += 1
        self.visited = True
        return True

class Nop(Instruction):
    pass

class Accumulate(Instruction):
    def __init__(self, data):
        super().__init__(data)

    def run(self, proc):
        if not super().run(proc):
            return False

        proc.accumulator += self.data
        return True

class Jump(Instruction):
    def __init__(self, data):
        super().__init__(data)

    def run(self, proc):
        if not super().run(proc):
            return False

        # -1, as base has already stepped one instruction
        proc.instruction += (self.data - 1)
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
        instr = Nop(val)
    elif op == "acc":
        instr = Accumulate(val)
    elif op == "jmp":
        instr = Jump(val)
    else:
        print("unrecognized op")


    program.append(instr)

def flip(i):
    if isinstance(program[i], Jump):
        program[i] = Nop(program[i].data)
    elif isinstance(program[i], Nop):
        program[i] = Jump(program[i].data)

length = len(program)
for i in range(7, length):

    flip(i)

    for r in program:
        r.visited = False

    proc = Processor(program)

    if proc.execute():
        print("program finished, accumulator", proc.accumulator)
        break

    # second flip resets state
    flip(i)

