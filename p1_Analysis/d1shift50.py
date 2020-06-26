#Shifting 50% rising point to align

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#Determining average index location of center 50% rising point
def center_check(Nloops,numhead,datadate):
    center_list = []  #initializing list
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i
        (_,y,_) = rw(filename,numhead)                          #reading in waveform y values
        y_norm = y/min(y[370:1370])                             #normalizing to make calculations easier
        check = y_norm >= 0.5                                   #50% crossing criteria
        index = [k for k, x in enumerate(check) if x]           #code to enumerate index values
        index_50 = int(index[0])                                #making into integer
        center_list = center_list.append(index_50)              #appending index location to list of index locations
    center_list = np.asarray(center_list)                       #converting list to numpy array
    center_list_sorted = np.sort(center_list)                   #sort center_list array
    max_index = int(round(center_list_sorted[(len(center_list_sorted)-1)]))     #determine maximum index
    min_index = int(round(center_list_sorted[0]))               #determine minimum index
    center_index = int(round(np.mean(center_list)))             #establishing mean index location, rounding it, and converting to integer
    return(max_index,min_index,center_index,center_list)

#shifting to align
def d1shift50(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted'))   #establishing size of direcory
    (max_index,min_index,center_index,center_list) = center_check(Nloops,numhead,datadate)          #checking for average location of 50% rise point
    #printing calculated indices
    print(min_index)
    print(center_index)
    print(max_index)
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered/'):          #creating write directory if nonexistant
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered/')
    for i in range(Nloops):
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i  #setting file name for reading
        writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i       #setting file name for writing
        (t,y,header) = rw(filename,numhead)                               #reading in waveform values
        index_50 = int(center_list[i] + 0.5)                              #converting to int
        t_50 = t[index_50]                                          #converting index of 50% rising point to value at that point
        t_new = (t - t_50)                                          #shifting t_50 to t=0s
        #rolling so 50 rising point is at center index
        t_intermediate = np.roll(t_new,center_index - index_50)
        y_intermediate = np.roll(y,center_index - index_50)
        first_cutoff = (center_index - min_index)                   #determining latest first index
        last_cutoff = (len(y) - max_index + center_index)           #determining earliest last index
        #slicing off 'problem indices'
        t_50centered = t_intermediate[first_cutoff:last_cutoff]
        y_50centered = y_intermediate[first_cutoff:last_cutoff]
        write_waveform(t_50centered, y_50centered, writename, header)   #writing final waveform

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='d1shift50', description='Shifting 0.5 rising point to align')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    d1shift50(args.datadate,args.numhead)