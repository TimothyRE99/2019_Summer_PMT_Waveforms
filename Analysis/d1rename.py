#rename d1_raw files and move to new folder

#import necessary
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#moves files
numhead = 5
files = os.listdir('G:/data/watchman/20190516_watchman_spe/d1/d1_raw')          #creating list of files in d1_raw directory
for i in range(len(files)):
    filename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_raw/' + files[i]   #appending directory to filename values
    writename = 'G:/data/watchman/20190516_watchman_spe/d1/d1_renamed/D1--waveforms--%05d.txt' % i      #renaming files to correspond with position in directory and moving to new folder
    (t,y,header) = rw(filename,numhead)             #reading files from filename directory
    write_waveform(t,y,writename,header)            #writing files to writename directory