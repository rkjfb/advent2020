import numpy as np
a = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(a)

print("row+column")
print(a[:,0])
print(a[0,:])

print("transpose")
print(np.transpose(a))

print("rot90")
print(np.rot90(a, k=1, axes=(0, 1)))
print(np.rot90(a, k=1, axes=(1, 0)))

print("flip")
print(np.flip(a))

b = dict()
b[1] = 2
for c in b:
    print(c)

print("iterate")

m = a
for i in range(4):
    m = np.rot90(m)
    print(m[0,:])
m = np.fliplr(a)
for i in range(4):
    m = np.rot90(m)
    print(m[0,:])

