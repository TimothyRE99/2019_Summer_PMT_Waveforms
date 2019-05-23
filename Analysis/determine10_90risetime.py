#Determining 10-90 rise time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh
import os

def determine(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted'))
    writename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/10_90_rise_time.txt'
    #determine rise times
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y[370:1370])
        check10 = y_norm >= .1                                      #determining where 10% and 90% are located
        check90 = y_norm >= .9
        index10 = [k for k, x in enumerate(check10) if x]
        index_10 = int(index10[0])
        index90 = [k for k, x in enumerate(check90) if x]
        index_90 = int(index90[0])
        rise_time = str(t[index_90] - t[index_10])                  #rise time is time at 90% - time at 10%
        wh(rise_time,writename)
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Seconds","Histogram of 10-90 Rise Times","10_90_Rise",data_date,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determine10_90risetime', description='determining and writing histogram for 10-90 rise times')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.data_date,args.numhead)