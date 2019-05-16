#Determining 20-80 fall time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
import os

#Setting variables
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d1/d1_baseline_shifted'))
numhead = 5
writename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_histograms/20_80_fall_time.txt'

#determine fall times
for i in range(Nloops):
    filename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
    (t,y,_) = rw(filename,numhead)
    y_norm = y/min(y[370:1370])
    check20 = y_norm >= .2                                          #determining where 20% and 80% falling are located
    check80 = y_norm >= .8
    index20 = [k for k, x in enumerate(check20) if x]
    index_20 = int(index20[len(index20)-1])
    index80 = [k for k, x in enumerate(check80) if x]
    index_80 = int(index80[len(index80)-1])
    fall_time = str(t[index_20] - t[index_80])                      #fall time is time at 20% - time at 80%
    wh(fall_time,writename)