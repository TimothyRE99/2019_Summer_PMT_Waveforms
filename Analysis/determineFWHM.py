#Determining 20-80 rise time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
import os

#Setting variables
Nloops = len(os.listdir('G:/data/watchman/20190514_watchman_spe/d1/d1_baseline_shifted'))
numhead = 5
writename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_histograms/FWHM.txt'

#determine rise times
for i in range(Nloops):
    filename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
    (t,y,_) = rw(filename,numhead)
    y_norm = y/min(y[370:1370])
    check = y_norm >= .5                                #determining where 50% falling and rising are located
    index = [k for k, x in enumerate(check) if x]
    index_first = int(index[0])
    index_last = int(index[len(index)-1])
    FWHM = (t[index_last] - t[index_first])        #FWHM is time at falling 50% - time at rising 50%
    wh(FWHM,writename)