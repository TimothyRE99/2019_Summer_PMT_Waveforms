#Remove baseline from files to line up closer to 0

#import necessay
import numpy as np
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#shift baseline
Nloops = len(os.listdir('G:/data/watchman/20190514_watchman_spe/d1/d1_renamed'))
numhead = 5
for i in range(Nloops):
    filename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_renamed/D1--waveforms--%05d.txt' % i
    writename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
    (t,y,header) = rw(filename,numhead)
    baseline = np.mean(y[0:200])
    y_new = (y - baseline)
    write_waveform(t,y_new,writename,header)