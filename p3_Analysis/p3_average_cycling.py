#takes average waveforms, gains to same height, runs p3 on it

#import necessary
import numpy as np
import os
import random
import math
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#gain
def gain(v,v2,v4,v8):
    factor = -.0063283/max(v)
    factor2 = -.0063283/max(v2)
    factor4 = -.0063283/max(v4)
    factor8 = -.0063283/max(v8)
    v = v * factor
    v2 = v2 * factor2
    v4 = v4 * factor4
    v8 = v8 * factor8
    return(v,v2,v4,v8)

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
def downsampling(t,v,fsps,new_fsps):
    steps = int(fsps/new_fsps + 0.5)                                #determining how many 'steps' from original waveform can be taken
    start_index = random.randint(0,steps - 1)                       #randomly determining start index within range [0,steps)
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
def p3_average_cycling(datadate,numhead,fsps,new_fsps,noise):
    filedir = 'G:/Data/watchman/'+datadate+'_watchman_spe/d2/'
    writedir1 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d3/d3_averages/raw/'
    writedir2 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d3/d3_averages/rise_doubled/'
    writedir4 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d3/d3_averages/rise_quadrupled/'
    writedir8 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d3/d3_averages/rise_octupled/'
    if not os.path.exists(writedir1):
        os.makedirs(writedir1)
    if not os.path.exists(writedir2):
        os.makedirs(writedir2)
    if not os.path.exists(writedir4):
        os.makedirs(writedir4)
    if not os.path.exists(writedir8):
        os.makedirs(writedir8)
    filename1 = filedir + 'd2_average.txt'
    filename2 = filedir + 'd2_average_doubled.txt'
    filename4 = filedir + 'd2_average_quadrupled.txt'
    filename8 = filedir + 'd2_average_octupled.txt'
    (t,v,header) = rw(filename1,numhead)
    (t2,v2,header2) = rw(filename2,numhead)
    (t4,v4,header4) = rw(filename4,numhead)
    (t8,v8,header8) = rw(filename8,numhead)
    (v,v2,v4,v8) = gain(v,v2,v4,v8)
    Nloops = 10000
    for i in range(Nloops):
        print(i)
        writename1 = writedir1 + 'D3--waveforms--%05d.txt' % i
        writename2 = writedir2 + 'D3--waveforms--%05d.txt' % i
        writename4 = writedir4 + 'D3--waveforms--%05d.txt' % i
        writename8 = writedir8 + 'D3--waveforms--%05d.txt' % i
        #downsampling waveform values
        (t_down_1,v_down_1) = downsampling(t,v,fsps,new_fsps)
        (t_down_2,v_down_2) = downsampling(t2,v2,fsps,new_fsps)
        (t_down_4,v_down_4) = downsampling(t4,v4,fsps,new_fsps)
        (t_down_8,v_down_8) = downsampling(t8,v8,fsps,new_fsps)
        #digitizing waveform values
        v_digit_1 = digitize(v_down_1,noise)
        v_digit_2 = digitize(v_down_2,noise)
        v_digit_4 = digitize(v_down_4,noise)
        v_digit_8 = digitize(v_down_8,noise)
        #saving downsampled and digitized waveforms
        write_waveform(t_down_1,v_digit_1,writename1,header)
        write_waveform(t_down_2,v_digit_2,writename2,header2)
        write_waveform(t_down_4,v_digit_4,writename4,header4)
        write_waveform(t_down_8,v_digit_8,writename8,header8)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p3 average cycling",description="Downsamples and digitizes average waveforms.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--new_fsps",type=float,help="hz, samples/s of new digitizer",default=125000000.0)
    parser.add_argument("--noise",type=float,help='bits of noise from digitizer',default=3.3)
    args = parser.parse_args()

    p3_average_cycling(args.datadate,args.numhead,args.fsps,args.new_fsps,args.noise)