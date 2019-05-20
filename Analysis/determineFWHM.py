#Determining 20-80 rise time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
import os

def determine(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted'))
    writename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/FWHM.txt'
    #determine rise times
    for i in range(Nloops):
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y[370:1370])
        check = y_norm >= .5                                #determining where 50% falling and rising are located
        index = [k for k, x in enumerate(check) if x]
        index_first = int(index[0])
        index_last = int(index[len(index)-1])
        FWHM = str(t[index_last] - t[index_first])          #FWHM is time at falling 50% - time at rising 50%
        wh(FWHM,writename)
    #create histogram from saved file
    rh(writename,"Seconds","Histogram of Full Width Half Maximums","FWHM",data_date)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determineFWHM', description='determining and writing histogram for FWHMs')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.data_date,args.numhead)