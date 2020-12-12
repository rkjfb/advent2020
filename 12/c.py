import numpy as np

v = np.array([1,2,0])
np.rot90(v, 1, [0,0,1])
print(v)

