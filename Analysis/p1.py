#import necessary
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os
from p1sort import p1_sort

def p1(NLoops, data_date, numhead, fsps, fc, numtaps, j, threshold, baseline):
    wc = 2.*np.pi*fc/fsps   #discrete radial frequency
    lowpass = signal.firwin(numtaps, cutoff = wc/np.pi, window = 'blackman')    #blackman windowed lowpass filter
    for i in range(j, NLoops):
        p1_sort(i,data_date,lowpass,numhead,numtaps,threshold,baseline)          #running p1_sort function to sort files

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='p1', description='Calculating lowpass filter and calling p1_sort')
    parser.add_argument('--NLoops',type = int,help = 'number of files to circle through',default = 100000)
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--fsps',type=int,help='hz, samples/s',default = 20000000000)
    parser.add_argument('--fc',type=int,help='hz, cutoff frequency',default = 250000000)
    parser.add_argument('--numtaps',type=int,help='length of filter',default = 51)
    parser.add_argument('--j',type=int,help='starting file number',default=0)
    parser.add_argument('--threshold',type = int,help='voltage threshold',default=-0.0015)
    parser.add_argument('--baseline',type = int,help='baseline voltage',default=0)
    args = parser.parse_args()

    p1(args.NLoops, args.data_date, args.numhead, args.fsps, args.fc, args.numtaps, args.j, args.threshold, args.baseline)