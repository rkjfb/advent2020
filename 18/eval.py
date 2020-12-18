import re

class Silly(int):
    def __add__(self, other):
        # double flip, so we get original intended operation
        return Silly(super().__mul__(other))
    def __mul__(self, other):
        return Silly(super().__add__(other))

# basic eval
s = "1 + 2 * 3 + 4 * 5 + 6"
print(eval(s))

# introduce a new type so we can override operators
n = re.sub("(\d)", "Silly(\\1)", s)

# flip the operators to python executes in standard order
nn = n.replace("+", "-")
nn = nn.replace("*", "+")
nn = nn.replace("-", "*")

print("expect231", eval(nn))
