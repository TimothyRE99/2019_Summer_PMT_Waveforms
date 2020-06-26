import numpy as np
import os
import random
import math
from readwaveform import read_waveform as rw
from writewaveform import write_waveform as ww
import scipy.interpolate as it
from unispline import unispline as us

#digitizing
def digitize(v,noise):
    v_new = np.array([])
    for i in range(len(v)):
        v_new = np.append(v_new,(v[i] * (2**14 - 1)*2 + 0.5))           #multiplying by digitizer formula to convert to bits
    noise_array = np.random.normal(loc=0.0, scale = noise, size = len(v_new))       #generating noise array
    v_final = np.add(v_new, noise_array)    #adding noise to digitized values
    v_final = v_final.astype(int)           #converting values to ints
    return(v_final)

#downsampling
def downsampling(t,v,fsps,new_fsps,start_index):
    steps = int(fsps/new_fsps + 0.5)                                #determining how many 'steps' from original waveform can be taken
    multiplier = math.floor((len(v) - start_index - 1) / steps)     #determining max amount you can multiply the steps value by and add onto the start value without overshooting end of array
    #initializing arrays
    t_new = np.array([])
    v_new = np.array([])
    #grabbing only values of array that the digitizer would grab
    for i in range(multiplier + 1):
        t_new = np.append(t_new,t[start_index + i * steps])
        v_new = np.append(v_new,v[start_index + i * steps])
    return t_new,v_new

#reading and writing waveforms and calling other functions
def p3(new_fsps,datadate,numhead,scale_array,phase_array,noise,fsps,steps):
    #establishing directory names
    if new_fsps == 1000000000:
        sample_rate = '1 Gsps'
    elif new_fsps == 500000000:
        sample_rate = '500 Msps'
    elif new_fsps == 250000000:
        sample_rate = '250 Msps'
    else:
        sample_rate = 'trash'
    filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt'
    t,v,header = rw(filename,numhead)
    uspl = us(t,v)
    for i in range(len(phase_array)):
        print(i)
        writedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/averages_splined/phase=' + str(i) + '/phase_raw_gained_analyzed_unnoised/'
        #creating directories if they don't exist
        if not os.path.exists(writedir):
            os.makedirs(writedir)
        start_value = t[i]
        end_value = t[-1]
        t_array = np.arange(start_value,end_value,1/new_fsps)
        v_array = uspl(t_array)
        Nloops = len(scale_array)      #establishing how many files to cycle through
        for j in range(Nloops):
            scale_height = scale_array[j]/np.max(v_array)
            v_scaled = v_array*scale_height
            print('%s/%s, File: %05d' % (i + 1,steps,j))             #printing number of file currently being processed
            #establishing read and write names
            writename = writedir + 'Phase--waveforms--%05d.txt' % j
            #digitizing waveform values
            v_digit = digitize(v_scaled,noise)
            #saving downsampled and digitized waveforms
            ww(t_array-i/fsps,v_digit,writename,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="spline_discrete_copy",description="Runs Downsampling and Digitizing based on discrete phases for splined waveform.")
    parser.add_argument("--noise",type=float,help='bits of noise from digitizer',default=0)
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    args = parser.parse_args()

    new_fsps = 250000000
    scale_array = np.random.normal(-0.0065313,0.0018414,10000)
    phase_array = np.arange(0,1/new_fsps,1/args.fsps)
    steps = int(args.fsps/new_fsps + 0.5)
    p3(new_fsps,args.datadate,args.numhead,scale_array,phase_array,args.noise,args.fsps,steps)