#sorts voltage data and calculates difference between two numbers

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
import matplotlib.pyplot as plt

#calculating differences
def voltage_diff(v):
    v_differences = np.array([])
    for i in range(len(v)-1):
        v_differences = np.append(v_differences,v[i]-v[i+1])
    return v_differences

#reading in data and calling sort functions
def waveform_sort(filenum,datadate,numhead):
    filename = 'G:/data/watchman/'+datadate+'_watchman_spe/C2--waveforms--%05d.txt' % filenum
    (_,v,_) = rw(filename,numhead)
    v_sorted = np.flip(np.sort(v,kind = "mergesort"))
    v_differences = voltage_diff(v_sorted)
    min_v_diff = min(v_differences)
    max_v_diff = max(v_differences)
    plt.hist(v_differences, bins=np.arange(min_v_diff,max_v_diff+1.3729999999e-8,1.3729999999e-8), log = True)
    plt.show()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='waveform sort', description='sorting voltages, calculating differences, and showing minimum difference')
    parser.add_argument('--filenum',type = int,help = 'file to use',default = 1)
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    waveform_sort(args.filenum,args.datadate,args.numhead)