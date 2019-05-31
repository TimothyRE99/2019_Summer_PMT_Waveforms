#Read a waveform from a time, voltage CSV format

#import necessary
import numpy as np
import matplotlib.pyplot as plt
import os

#plot the data
def read_waveform(filename,numhead):
    fin = open(filename,'r')
    header = []
    x = np.array([])
    y = np.array([])
    for _ in range(numhead):
        header.append(fin.readline())
    for line in fin:
        x = np.append(x,float(line.split(',')[0]))
        y = np.append(y,float(line.split(',')[1]))
    fin.close
    return x,y,header

#for testing
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="read waveform",description="read the waveform datafile.")
    parser.add_argument("--numhead",type=int,help='number of header lines to skip in the raw file',default=5)
    parser.add_argument("--filename",type=str,help="filename",default='g:/data/watchman/20190514_watchman_spe/C2--waveforms--00000.txt')
    args = parser.parse_args()

    x,y,header = read_waveform(args.filename,args.numhead)
    print(header)
    plt.plot(x,y)
    plt.show()