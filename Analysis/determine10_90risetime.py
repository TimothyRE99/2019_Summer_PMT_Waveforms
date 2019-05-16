#Determining 10-90 rise time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
import os

#Setting variables
Nloops = len(os.listdir('G:/data/watchman/20190514_watchman_spe/d1/d1_baseline_shifted'))
numhead = 5
writename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_histograms/10_90_rise_time.txt'

#determine rise times
for i in range(Nloops):
    filename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
    (t,y,_) = rw(filename,numhead)
    y_norm = y/min(y[370:1370])
    check10 = y_norm >= .1
    check90 = y_norm >= .9
    index10 = [k for k, x in enumerate(check10) if x]
    index_10 = int(index10[0])
    index90 = [k for k, x in enumerate(check90) if x]
    index_90 = int(index90[0])
    rise_time = (t[index_90] - t[index_10])
    wh(rise_time,writename)