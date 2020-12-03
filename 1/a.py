data = open("data.txt", "r")
lines = data.readlines()
myints = []
for line in lines:
    i = int(line)
    myints.append(i)

for x in myints:
    for y in myints:
        for z in myints:
            if x+y+z == 2020:
                print("x", x, "y", y, "z", z, x+y+z, x*y*z)

