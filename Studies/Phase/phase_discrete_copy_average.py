#copying and downsampling/digitizing waveforms from p2 with discrete phases


#import necessary
import numpy as np
import os
import random
import math
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

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
def p3(noise,datadate,numhead,fsps,new_fsps,gain_noise,gain_factor_2,gain_factor_4,gain_factor_8,start_index,steps,scale_array):
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
    writedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/averages/phase=' + str(start_index) + '/phase_raw_gained_analyzed/'
    #creating directories if they don't exist
    if not os.path.exists(writedir):
        os.makedirs(writedir)
    t,v,header = rw(filename,numhead)
    Nloops = len(scale_array)      #establishing how many files to cycle through
    for i in range(Nloops):
        scale_height = scale_array[i]/np.max(v)
        v_scaled = v*scale_height
        print('%s/%s, File: %05d' % (start_index + 1,steps,i))             #printing number of file currently being processed
        #establishing read and write names
        writename = writedir + 'Phase--waveforms--%05d.txt' % i
        #downsampling waveform values
        (t_down,v_down) = downsampling(t-start_index*1/20000000000,v_scaled,fsps,new_fsps,start_index)
        #digitizing waveform values
        v_digit = digitize(v_down,noise)
        #saving downsampled and digitized waveforms
        write_waveform(t_down,v_digit,writename,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="phase_discrete_copy_average",description="Runs Downsampling and Digitizing based on discrete phases for average waveform.")
    parser.add_argument("--noise",type=float,help='bits of noise from digitizer',default=3.3)
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--gain_noise",type=float,help="standard deviation of noise gaussian for gain step",default=0)
    parser.add_argument("--gain_factor_2",type=float,help="Factor to multiply doubled by",default=2.9702411538)
    parser.add_argument("--gain_factor_4",type=float,help="Factor to multiply quadrupled by",default=3.9455513908)
    parser.add_argument("--gain_factor_8",type=float,help="Factor to multiply octupled by",default=7.3329373547)
    args = parser.parse_args()

    new_fsps = np.array([250000000])
    scale_array = np.random.normal(-0.0065313,0.0018414,10000)
    for i in range(len(new_fsps)):
        steps = int(args.fsps/new_fsps[i] + 0.5)
        for j in range(steps):
            start_index = j
            p3(args.noise,args.datadate,args.numhead,args.fsps,new_fsps[i],args.gain_noise,args.gain_factor_2,args.gain_factor_4,args.gain_factor_8,start_index,steps,scale_array)