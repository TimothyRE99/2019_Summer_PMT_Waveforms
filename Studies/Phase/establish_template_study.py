#Establishes files for investigation of using Template Waveform with different variations

#Import necessary
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

#Function that calls most other functions, runs small calculations
def establish_templates(new_fsps,datadate,numhead,scale_array,phase_array,noise,fsps,steps,scale_mean):
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
        writedir_noise = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/file_template/phase=' + str(i) + '/phase_raw_gained_analyzed_noised/'
        writedir_peaked = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/file_template/phase=' + str(i) + '/phase_raw_gained_analyzed_peaked/'
        #creating directories if they don't exist
        if not os.path.exists(writedir_noise):
            os.makedirs(writedir_noise)
        if not os.path.exists(writedir_peaked):
            os.makedirs(writedir_peaked)
        start_value = t[i]
        end_value = t[-1]
        t_array = np.arange(start_value,end_value,1/new_fsps)
        v_array = uspl(t_array)
        Nloops = len(scale_array)      #establishing how many files to cycle through
        for j in range(Nloops):
            scale_height_noise = scale_mean/np.max(v_array)
            scale_height_peaked = scale_array[j]/np.max(v_array)
            v_scaled_noise = v_array*scale_height_noise
            v_scaled_peaked = v_array*scale_height_peaked
            print('%s/%s, File: %05d' % (i + 1,steps,j))             #printing number of file currently being processed
            #establishing read and write names
            writename_noise = writedir_noise + 'Phase--waveforms--%05d.txt' % j
            writename_peaked = writedir_peaked + 'Phase--waveforms--%05d.txt' % j
            #digitizing waveform values
            v_digit_noise = digitize(v_scaled_noise,noise)
            v_digit_peaked = digitize(v_scaled_peaked,noise)
            #saving downsampled and digitized waveforms
            ww(t_array-i/fsps,v_digit_noise,writename_noise,header)
            ww(t_array-i/fsps,v_digit_peaked,writename_peaked,header)
    return()

#Main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="",description="")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument("--noise",type=float,help='bits of noise from digitizer',default=3.3)
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument('--new_fsps',type=int,help='samples per second',default = 250000000)
    args = parser.parse_args()

    scale_mean = -0.0065414
    scale_std = 0.0018414
    scale_array = np.random.normal(scale_mean,scale_std,10000)
    j = 0
    while np.amin(scale_array) > 0:
        print(str(j) + ', ' + str(np.amin(scale_array)))
        scale_array = np.random.normal(scale_mean,scale_std,10000)
        j += 1
    phase_array = np.arange(0,1/args.new_fsps,1/args.fsps)
    steps = int(args.fsps/args.new_fsps + 0.5)
    establish_templates(args.new_fsps,args.datadate,args.numhead,scale_array,phase_array,args.noise,args.fsps,steps,scale_mean)