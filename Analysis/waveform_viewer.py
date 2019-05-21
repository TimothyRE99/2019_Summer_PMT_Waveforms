#cycle through viewing all the waveforms in a particular directory

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw
from scipy import signal
import os

#cycle through
def waveform_viewer(data_date,subfolder_name,numhead):
    NLoops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/'+subfolder_name))          #determine number of files in directory
    files = os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/'+subfolder_name)                #create list of file names in directory
    for i in range(NLoops):                                                                             #cycle through number of files
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/'+subfolder_name+'/'+files[i]        #open first file in list
        (x,y,_) = rw(filename,numhead)                  #get data from file, ignore header
        print(filename)                                 #print name of file
        plt.plot(x,y)                                   #plot data from file
        plt.title(files[i])                             #title plot with name of file
        plt.show()                                      #show plot, with pause in code

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determine10_90falltime', description='determining and writing histogram for 10-90 fall times')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--subfolder_name',type = str,help = 'subfolder to cycle through',default = 'unsure_if_spe')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    waveform_viewer(args.data_date,args.subfolder_name,args.numhead)