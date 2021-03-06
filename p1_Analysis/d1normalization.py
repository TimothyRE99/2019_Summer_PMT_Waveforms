#Normalize d1 csv's so peak = 1 and baseline = 0

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#normalization of data
def d1normalization(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered')) #establishing size of directory
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_normalized/'):  #creating write directory if nonexistant
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_normalized/')
    for i in range(Nloops):
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i    #setting file name for reading
        writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_normalized/D1--waveforms--%05d.txt' % i   #setting file name for writing
        (t,y,header) = rw(filename,numhead) #gathering waveform data into array
        y_norm = y/min(y)                                 #normalizing y to peak = 1
        write_waveform(t,y_norm,writename,header)   #writing normalized waveform

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='d1normalization', description='Normalizing the data')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    d1normalization(args.datadate,args.numhead)