#lowpass filter calculation for use in p2

#import necessary
import numpy as np
import matplotlib.pyplot as plt

#low pass filter
def lpfFirstOrder(v,tau,fsps):
    alpha = 1-np.exp(-1/(fsps*tau))
    y = np.zeros(len(v))
    for i in range(len(v)):
        if i == 0:
            y[i] = v[i]
        else:
            y[i] = v[i]*alpha + (1-alpha)*y[i-1]
    return y