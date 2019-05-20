#Determining charge of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
import os

def determine(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted'))
    writename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/charge.txt'
    #determining charge
    for i in range(Nloops):
        area = 0
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y_norm = y/min(y[370:1370])
        check = y_norm >= 0.1                                   #setting curve to be from 10% rising to 10% falling
        index = [k for k, x in enumerate(check) if x]
        for i in range(len(index)-1):
            area += ((t[i+1]-t[i]) * y[i])                      #determining area under curve
        charge = str(area/50)                                   #area under curve/resistance gives charge
        wh(charge,writename)
    #create histogram from saved file
    rh(writename,"Volts","Histogram of Charges","Charge",data_date)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determinecharge', description='determining and writing histogram for charges')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.data_date,args.numhead)