import numpy as np
from readwaveform import read_waveform as rw
import matplotlib.pyplot as plt
import scipy.interpolate as it

def unispline(t,v):
    length = len(t)
    w = np.zeros(length)
    w = w + 1000
    uspl = it.UnivariateSpline(t,v,w=w,k=5)
    return(uspl)


filename = 'G:/data/watchman/20190724_watchman_spe/d2/d2_average.txt'
t,v,_ = rw(filename,1)
uspl = unispline(t,v)
x = np.linspace(t[0],t[-1],10000)
y = uspl(x)

plt.xlim(t[0] - 20*(t[1] - t[0]),t[-1] + 20*(t[1] - t[0]))
plt.scatter(t,v)
plt.plot(x,y)
plt.get_current_fig_manager().window.showMaximized()
plt.show()