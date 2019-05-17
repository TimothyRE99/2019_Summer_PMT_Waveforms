#determine peak amplitude of waveform

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh

#define constants
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d1/d1_baseline_shifted'))
numhead = 5
writename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_histograms/peak_amplitude.txt'

#peak amplitude acquisition
for i in range(Nloops):
    filename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
    (_,y,_) = rw(filename,numhead)
    index_min = np.where(y == min(y[370:1370]))                     #determining index of peak
    value = str((-1*y[index_min])[0])                               #flipping peak to positive
    wh(value,writename)

#create histogram from saved file
rh(writename,"Volts","Histogram of Peak Amplitudes","Peak_Amplitude")