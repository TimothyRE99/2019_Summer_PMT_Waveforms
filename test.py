import numpy as np

y = np.array([1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1])
check = y >= 5
index = [k for k, x in enumerate(check) if x]
print(index)
index_last = int(index[len(index)-1])
print(index_last)