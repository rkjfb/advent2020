import re
import json

class Processor:
    def __init__(self):
        self.accumulator = 0
        self.instruction = 0
        self.program = []

    # Returns true if program completes execution
    def execute(self):
        length = len(self.program)
        while not self.instruction == length:
            # TODO:
            # - Instruction base class, that does base things like increment instruction
            # - execute() on an instructions should update processor state somehow. return tuple? processor argument?
            ret = self.program[self.instruction].run()
            if not ret:
                break

        if instruction == length:
            return True

        return False


#TODO: learn python abc class inherit
class Nop:
    def __init__(self, skip):
        # skip is not used by nop, just for type switching with Jump
        self.skip = skip
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
        program[i] = Nop(program[i].skip)
    elif isinstance(program[i], Nop):
        program[i] = Jump(program[i].skip)

length = len(program)
for i in range(length):

    flip(i)

    # reset program state
    accumulator = 0
    instruction = 0

    for r in program:
        r.visited = False

    while not instruction == length:
        ret = program[instruction].run()
        #print("instruction", instruction, "ret", ret)
        if not ret:
            break

    if instruction == length:
        print("program finished at instruction", i)
        break

    # second flip resets state
    flip(i)


print("accumulator", accumulator)
