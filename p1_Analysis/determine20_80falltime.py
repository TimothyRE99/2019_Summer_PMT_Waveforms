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
    writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/20_80_fall_time.txt'
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/histogram_images'):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/histogram_images')
    #determine fall times
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y)
        check20 = y_norm <= .2                                          #determining where 20% and 80% falling are located
        check80 = y_norm >= .8
        index20 = np.asarray([k for k, x in enumerate(check20) if x])
        index80 = np.asarray([k for k, x in enumerate(check80) if x])
        index_80 = int(index80[len(index80)-1] + 0.5)
        index20_removed = index20[np.where(index20 > index_80)]         #removing all values after 80% fall index
        index_20 = index20_removed[0]                                   #turning first 20% fall index into int
        fall_time = str(t[index_20] - t[index_80])                      #fall time is time at 20% - time at 80%
        wh(fall_time,writename)                                         #writing value to histogram txt file
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Seconds","Histogram of 20-80 Fall Times","20_80_Fall",datadate,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determine20_80falltime', description='determining and writing histogram for 20-80 fall times')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.datadate,args.numhead)