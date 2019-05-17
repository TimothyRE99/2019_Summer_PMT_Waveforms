#Determining 20-80 fall time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
import os

#Setting variables
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d1/d1_baseline_shifted'))
numhead = 5
writename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_histograms/10_90_fall_time.txt'

#determine fall times
for i in range(Nloops):
    filename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
    (t,y,_) = rw(filename,numhead)
    y_norm = y/min(y[370:1370])
    check10 = y_norm >= .1                                          #determining where 10% and 90% falling are located
    check90 = y_norm >= .9
    index10 = [k for k, x in enumerate(check10) if x]
    index_10 = int(index10[len(index10)-1])
    index90 = [k for k, x in enumerate(check90) if x]
    index_90 = int(index90[len(index90)-1])
    fall_time = str(t[index_10] - t[index_90])                      #fall time is time at 10% - time at 90%
    wh(fall_time,writename)

#create histogram from saved file
rh(writename,"Seconds","Histogram of 10-90 Fall Times","10_90_Fall")