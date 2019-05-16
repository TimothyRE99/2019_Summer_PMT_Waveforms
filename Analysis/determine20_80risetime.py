#Determining 20-80 rise time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
import os

#Setting variables
Nloops = len(os.listdir('G:/data/watchman/20190514_watchman_spe/d1/d1_baseline_shifted'))
numhead = 5
writename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_histograms/20_80_rise_time.txt'

#determine rise times
for i in range(Nloops):
    filename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
    (t,y,_) = rw(filename,numhead)
    y_norm = y/min(y[370:1370])
    check20 = y_norm >= .2
    check80 = y_norm >= .8
    index20 = [k for k, x in enumerate(check20) if x]
    index_20 = int(index20[0])
    index80 = [k for k, x in enumerate(check80) if x]
    index_80 = int(index80[0])
    rise_time = (t[index_80] - t[index_20])
    wh(rise_time,writename)