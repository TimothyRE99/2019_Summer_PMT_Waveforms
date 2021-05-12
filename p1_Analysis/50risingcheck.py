#check location of 50% point on rising edge
import numpy as np
from readwaveform import read_waveform as rw
import os

Nloops = len(os.listdir('G:/data/watchman/20190724_watchman_spe/d1/d1_baseline_shifted')) #establish size of directory
for i in range(Nloops):
    filename = 'G:/data/watchman/20190724_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i  #open specific file
    (_,y,_) = rw(filename,5)    #read in y values from the file
    y_norm = y/min(y[370:1370])                             #normalizing to make calculations easier
    check = y_norm >= 0.5                                   #50% crossing criteria
    index = [k for k, x in enumerate(check) if x]           #code to enumerate index values
    index50 = int(index[0] + 0.5)   #converting first index to an integer
    if index50 < 370:
        print(str(index50)+', '+str(filename))