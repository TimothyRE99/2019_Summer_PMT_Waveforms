#rename d1_raw files and move to new folder

#import necessary
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#moves files
numhead = 5
files = os.listdir('G:/data/watchman/20190514_watchman_spe/d1/d1_raw')
for i in range(len(files)):
    filename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_raw/' + files[i]
    writename = 'G:/data/watchman/20190514_watchman_spe/d1/d1_renamed/D1--waveforms--%05d.txt' % i
    (t,y,header) = rw(filename,numhead)
    write_waveform(t,y,writename,header)