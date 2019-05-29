#determine peak amplitude of waveform

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh

def determine(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_50centered'))
    writename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/peak_amplitude.txt'
    #peak amplitude acquisition
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
        (_,y,_) = rw(filename,numhead)
        index_min = np.where(y == min(y))                     #determining index of peak
        value = str((-1*y[index_min])[0])                               #flipping peak to positive
        wh(value,writename)
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Volts","Histogram of Peak Amplitudes","Peak_Amplitude",data_date,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determinepeakamplitude', description='determining and writing histogram for peak amplitudes')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.data_date,args.numhead)