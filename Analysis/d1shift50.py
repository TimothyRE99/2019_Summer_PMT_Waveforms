#Shifting 50% rising point to align

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#Determining average index location of center 50% rising point
def center_check(Nloops,numhead,data_date):
    center_list = np.array([])
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (_,y,_) = rw(filename,numhead)
        y_norm = y/min(y[370:1370])                             #normalizing to make calculations easier
        check = y_norm >= 0.5                                   #50% crossing criteria
        index = [k for k, x in enumerate(check) if x]           #code to enumerate index values
        index_50 = int(index[0])                                #converting to integer
        center_list = np.append(center_list,index_50)           #appending index location to list of index locations
    center_index = int(round(np.mean(center_list)))             #establishing mean index location, rounding it, and converting to integer
    return(center_index)

#shifting to align
def d1shift50(data_date,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted'))
    center_index = center_check(Nloops,numhead,data_date)
    for i in range(Nloops):
        filename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        writename = 'G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
        (t,y,header) = rw(filename,numhead)
        y_norm = y/min(y[370:1370])
        check = y_norm >= 0.5
        index = [k for k, x in enumerate(check) if x]
        index_50 = int(index[0])
        t_50 = t[index_50]
        t_new = (t - t_50)                                          #shifting t_50 to t=0s
        t_50centered = np.roll(t_new, center_index - index_50)      #rolling data vectors to align along common point
        y_50centered = np.roll(y, center_index - index_50)
        write_waveform(t_50centered, y_50centered, writename, header)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='d1shift50', description='Shifting 0.5 rising point to align')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    d1shift50(args.data_date,args.numhead)