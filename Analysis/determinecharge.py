#Determining charge of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh
import os

def determine(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted'))
    writename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/charge.txt'
    #determining charge
    for i in range(Nloops):
        print(i)
        area = 0
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y)
        check = y_norm >= 0.1                                   #setting curve to be from 10% rising to 10% falling
        check_checker = y_norm <= 0.1
        check_peak = y_norm == 1                                #determining peak location
        index_pre = np.asarray([k for k, x in enumerate(check) if x])
        index_checker = np.asarray([k for k, x in enumerate(check_checker) if x])
        index_peak = np.asarray([k for k, x in enumerate(check_peak) if x])
        peak_index = int(index_peak[0])                         #making peak location an integer
        index_checker_low = index_checker[np.where(index_checker < peak_index)]
        index_checker_high = index_checker[np.where(index_checker > peak_index)]
        low_index = int(index_checker_low[len(index_checker_low)-1])
        high_index = int(index_checker_high[0])
        index = index_pre[low_index:high_index+1]
        #determining area under curve
        for i in range(len(index)-1):
            area += ((t[index[i+1]]-t[index[i]]) * y[index[i]])
        charge = -1*str(area/50)                                #area under curve/resistance gives charge, made positive for graphical reasons
        wh(charge,writename)
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Coulombs","Histogram of Charges","Charge",data_date,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determinecharge', description='determining and writing histogram for charges')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.data_date,args.numhead)