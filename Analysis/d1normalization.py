#Normalize d1 csv's so peak = 1 and baseline = 0

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#define constants
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d1/d1_50centered'))
numhead = 5

#normalization
for i in range(Nloops):
    filename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
    writename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_normalized/D1--waveforms--%05d.txt' % i
    (t,y,header) = rw(filename,numhead)
    y_norm = y/min(y[370:1370])                                 #normalizing y to peak = 1
    write_waveform(t,y_norm,writename,header)