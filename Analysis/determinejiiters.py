#determine jitters of waveform

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh

def determine(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_50centered'))
    writename10 = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/10_jitter.txt'
    writename20 = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/20_jitter.txt'
    writename80 = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/80_jitter.txt'
    writename90 = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/90_jitter.txt'
    #peak amplitude acquisition
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y)
        check10 = y_norm <= .1                                      #determining where 10% and 90% are located
        check90 = y_norm >= .9
        index10 = np.asarray([k for k, x in enumerate(check10) if x])
        index90 = np.asarray([k for k, x in enumerate(check90) if x])
        index_90 = int(index90[0])
        index10_removed = index10[np.where(index10 < index_90)]
        index_10 = int(index10_removed[len(index10_removed)-1])
        check20 = y_norm <= .2                                          #determining where 20% and 80% rising are located
        check80 = y_norm >= .8
        index20 = np.asarray([k for k, x in enumerate(check20) if x])
        index80 = np.asarray([k for k, x in enumerate(check80) if x])
        index_80 = int(index80[0])
        index20_removed = index20[np.where(index20 < index_80)]
        index_20 = int(index20_removed[len(index20_removed)-1])
        t10 = str(t[index_10])
        t20 = str(t[index_20])
        t80 = str(t[index_80])
        t90 = str(t[index_90])
        wh(t10,writename10)
        wh(t20,writename20)
        wh(t80,writename80)
        wh(t90,writename90)
    (histo_mean10,histo_std10) = gh(writename10)
    (histo_mean20,histo_std20) = gh(writename20)
    (histo_mean80,histo_std80) = gh(writename80)
    (histo_mean90,histo_std90) = gh(writename90)
    rh(writename10,"Seconds","Histogram of 10% Jitter","10_Jitter",data_date,histo_mean10,histo_std10)
    rh(writename20,"Seconds","Histogram of 20% Jitter","20_Jitter",data_date,histo_mean20,histo_std20)
    rh(writename80,"Seconds","Histogram of 80% Jitter","80_Jitter",data_date,histo_mean80,histo_std80)
    rh(writename90,"Seconds","Histogram of 90% Jitter","90_Jitter",data_date,histo_mean90,histo_std90)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determinepeakamplitude', description='determining and writing histogram for peak amplitudes')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.data_date,args.numhead)