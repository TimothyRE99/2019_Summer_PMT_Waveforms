#import necessary
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import time
import os
from p1sort import p1_sort

#signal parameters (Unsure why needed, saving for potential future use)
show_plot = False
N = 4002                #signal window size
fsps = 20000000000      #hz, samples/s
NLoops = 10829          #number of files (This one is needed for p1_sort)
vthr = -0.00025
nhdr = 5                #size of header to ignore

#parameters for the filter (Also unsure why needed)
fc = 250000000          #hz, filter cutoff frequency
wc = 2.*np.pi*fc/fsps   #discrete radial frequency
print('wc',wc)
numtaps = 51            #filter order + 1, chosen for balance of good performance and small transient size
lowpass = signal.firwin(numtaps, cutoff = wc/np.pi, window = 'blackman')    #blackman windowed lowpass filter


j = 0
for i in range(j, NLoops):
    p1_sort(i)          #running p1_sort function to sort files