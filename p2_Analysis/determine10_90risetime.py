#Determining 10-90 rise time of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh
import os

def determine(datadate,numhead,directory):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_'+directory))
    if directory == 'raw':
        Nloops -= 1
    writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_histograms/10_90_rise_time_'+directory+'.txt'
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_histograms/histogram_images/'):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_histograms/histogram_images/')
    #determine rise times
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_'+directory+'/D2--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y)
        check10 = y_norm <= .1                                      #determining where 10% and 90% are located
        check90 = y_norm >= .9
        index10 = np.asarray([k for k, x in enumerate(check10) if x])
        index90 = np.asarray([k for k, x in enumerate(check90) if x])
        index_90 = int(index90[0] + 0.5)
        index10_removed = index10[np.where(index10 < index_90)]     #removing all values after 90% rise index
        index_10 = int(index10_removed[len(index10_removed)-1] + 0.5)   #turning last 10% rise index into int
        rise_time = str(t[index_90] - t[index_10])                  #rise time is time at 90% - time at 10%
        wh(rise_time,writename)                                     #writing value to histogram txt file
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Seconds","Histogram of 10-90 Rise Times","10_90_Rise_"+directory,datadate,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determine10_90risetime', description='determining and writing histogram for 10-90 rise times')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--directory',type=str,help='directory to look in',default = 'raw')
    args = parser.parse_args()

    determine(args.datadate,args.numhead,args.directory)