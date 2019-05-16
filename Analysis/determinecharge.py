#Determining charge of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
import os

#Setting variables
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d1/d1_baseline_shifted'))
numhead = 5
writename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_histograms/charge.txt'

#determining charge
for i in range(Nloops):
    area = 0
    filename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
    (t,y,header) = rw(filename,numhead)
    y_norm = y/min(y[370:1370])
    check = y_norm >= 0.1                                   #setting curve to be from 10% rising to 10% falling
    index = [k for k, x in enumerate(check) if x]
    for i in range(len(index)-1):
        area += ((t[i+1]-t[i]) * y[i])                      #determining area under curve
    charge = str(area/50)                                   #area under curve/resistance gives charge
    wh(charge,writename)