#Determining 20-80 fall time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh
import os

def determine(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted'))
    writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/10_90_fall_time.txt'
    #determine fall times
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y)
        check10 = y_norm <= .1                                          #determining where 10% and 90% falling are located
        check90 = y_norm >= .9
        index10 = np.asarray([k for k, x in enumerate(check10) if x])
        index90 = np.asarray([k for k, x in enumerate(check90) if x])
        index_90 = int(index90[len(index90)-1])
        index10_removed = index10[np.where(index10 > index_90)]         #removing all values before 90% fall index
        index_10 = int(index10_removed[0])                              #turning first 10% fall index into int
        fall_time = str(t[index_10] - t[index_90])                      #fall time is time at 10% - time at 90%
        wh(fall_time,writename)                                         #writing value to histogram txt file
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Seconds","Histogram of 10-90 Fall Times","10_90_Fall",datadate,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determine10_90falltime', description='determining and writing histogram for 10-90 fall times')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.datadate,args.numhead)