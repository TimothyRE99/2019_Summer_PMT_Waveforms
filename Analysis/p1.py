#import necessary
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import signal
sys.path.append("C:/Users/Timothy/Desktop/Summer Work/2019_Summer_PMT_Waveforms/Analysis")
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import time
import os
from p1sort import p1_sort

#signal parameters
show_plot = False
N = 4002                #signal window size
fsps = 20000000000      #hz, samples/s
NLoops = 10829
vthr = -0.00025
nhdr = 5

#parameters for the filter
fc = 250000000          #hz, filter cutoff frequency
wc = 2.*np.pi*fc/fsps   #discrete radial frequency
print('wc',wc)
numtaps = 51            #filter order + 1, chosen for balance of good performance and small transient size
lowpass = signal.firwin(numtaps, cutoff = wc/np.pi, window = 'blackman')    #blackman windowed lowpass filter


j = 0
for i in range(j, NLoops):
    p1_sort(i)