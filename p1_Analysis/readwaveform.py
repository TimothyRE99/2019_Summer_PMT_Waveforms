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
    parser.add_argument("--filename",type=str,help="filename",default='G:/data/watchman/20190724_watchman_spe/studies/phase/250 Msps/phase=0/phase_raw_gained_analyzed/Phase--waveforms--00000.txt')
    args = parser.parse_args()

    x,y,header = read_waveform(args.filename,args.numhead)
    print(header)
    FontSize = 32
    plt.rcParams.update({'font.size': FontSize})
    _,ax = plt.subplots()
    ax.plot(x,y,linewidth=4)
    ax.scatter(x,y,linewidth=4)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Bits')
    ax.set_title('250 MSPS Sample Waveform')
    plt.get_current_fig_manager().window.showMaximized()        #maximizes plot
    plt.show()