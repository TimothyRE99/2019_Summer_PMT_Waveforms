#cycle through viewing all the waveforms in a particular directory

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw
from scipy import signal
import os

#cycle through
def waveform_viewer(datadate,subfolder_name,numhead):
    NLoops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/'+subfolder_name))           #determine number of files in directory
    files = sorted(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/'+subfolder_name))         #create list of file names in directory
    plt.rcParams.update({'font.size': 14})
    for i in range(NLoops):                                                                             #cycle through number of files
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/'+subfolder_name+'/'+files[i]         #open first file in list
        (x,y,_) = rw(filename,numhead)                  #get data from file, ignore header
        y_line = min(y)*.5
        print(filename)                                 #print name of file
        plt.plot(x,y)                                   #plot data from file
        plt.axvline(x=0,color='red')
        plt.axhline(y=y_line,color='purple')
        plt.xlabel('Time (s)')
        plt.ylabel('Volts')
        plt.title('Sample SPE Waveform After P1:\nWaveform %05d' % i)                       #title plot with name of file
        plt.get_current_fig_manager().window.showMaximized()            #maximizes plot
        plt.show()                                      #show plot, with pause in code

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='waveformviewer', description='viewing all waveforms in a directory')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--subfolder_name',type = str,help = 'subfolder to cycle through',default = 'd1_final_spes')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    waveform_viewer(args.datadate,args.subfolder_name,args.numhead)