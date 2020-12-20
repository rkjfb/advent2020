import numpy as np
a = np.array([[1,2],[3,4]])
print(a)

print("row+column")
print(a[:,0])
print(a[0,:])

print("transpose")
print(np.transpose(a))

print("rot90")
print(np.rot90(a))

b = dict()
b[1] = 2
for c in b:
    print(c)
