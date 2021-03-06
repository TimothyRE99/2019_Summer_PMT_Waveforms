#Normalize d2 csv's so peak = 1 and baseline = 0

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#normalization of data
def d2normalization(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw'))
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_normalized/'):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_normalized/')
    for i in range(Nloops):
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/D2--waveforms--%05d.txt' % i
        writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_normalized/D2--waveforms--%05d.txt' % i
        (t,y,header) = rw(filename,numhead)
        y_norm = y/min(y)                                 #normalizing y to peak = 1
        write_waveform(t,y_norm,writename,header)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='d1normalization', description='Normalizing the data')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    d2normalization(args.datadate,args.numhead)