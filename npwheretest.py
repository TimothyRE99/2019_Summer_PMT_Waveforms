import numpy as np
test_array = np.array([1,2,3,4,5,6,7,8,9,10])
test_array_print = test_array[np.where(3 <= test_array <= 7)]
print(test_array_print)