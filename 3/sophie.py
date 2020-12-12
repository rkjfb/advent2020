data = open("data.txt", "r")
rawlines = data.readlines()
lines = [l.rstrip('\n') for l in rawlines]

print(lines[0][3]) row,col
print(lines[1][3])
print(lines[2][4])

print(type(lines)) # list
print(type(lines[0])) # str
print(type(lines[0][0])) # str
