#determine peak amplitude of waveform

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh

def determine(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw')) - 1
    writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_histograms/raw_peak_amplitude.txt'
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_histograms/histogram_images'):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_histograms/histogram_images')
    #peak amplitude acquisition
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/D2--waveforms--%05d.txt' % i
        (_,y,_) = rw(filename,numhead)
        index_min = np.where(y == min(y))               #determining index of peak
        value = str((-1*y[index_min])[0])               #flipping peak to positive
        wh(value,writename)                             #writing value to histogram txt file
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Volts","Histogram of Peak Amplitudes","Peak_Amplitude",datadate,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determinepeakamplitude', description='determining and writing histogram for peak amplitudes')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.datadate,args.numhead)