#Normalize d1 csv's so peak = 1 and baseline = 0

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#normalization of data
def d1normalization(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_50centered'))
    for i in range(Nloops):
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
        writename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_normalized/D1--waveforms--%05d.txt' % i
        (t,y,header) = rw(filename,numhead)
        y_norm = y/min(y)                                 #normalizing y to peak = 1
        write_waveform(t,y_norm,writename,header)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='d1normalization', description='Normalizing the data')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    d1normalization(args.data_date,args.numhead)