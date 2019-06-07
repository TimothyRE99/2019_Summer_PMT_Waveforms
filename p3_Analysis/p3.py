#downsample and digitize waveforms

#import necessary
import numpy as np
import os
import random
import math
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#digitizing
def digitize(v,noise):
    v_new = (v * (2**14 - 1)*2 + 0.5)
    noise_array = np.random.normal(loc=0.0, scale = noise, size = len(v_new))
    v_final = np.add(v_new, noise_array)
    return(v_final)

#downsampling
def downsampling(t,v,fsps,new_fsps):
    steps = fsps/new_fsps
    start_index = random.randint(0,steps - 1)
    multiplier = math.floor((len(v) - start_index - 1) / steps)
    t_new = np.array([])
    v_new = np.array([])
    for i in range(multiplier + 1):
        t_new = np.append(t_new,start_index + i * steps)
        v_new = np.append(v_new,start_index + i * steps)
    return t_new,v_new

#reading and writing waveforms and calling other functions
def p3(noise,datadate,numhead,fsps,new_fsps):
    if noise == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw/'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled/'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled/'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled/'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_analyzed/'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled_analyzed/'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled_analyzed/'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled_analyzed/'
    else:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_noise=' + str(noise) + 'V/'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled_noise=' + str(noise) + 'V/'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled_noise=' + str(noise) + 'V/'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled_noise=' + str(noise) + 'V/'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_analyzed_noise=' + str(noise) + 'V/'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled_analyzed_noise=' + str(noise) + 'V/'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled_analyzed_noise=' + str(noise) + 'V/'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled_analyzed_noise=' + str(noise) + 'V/'
    if not os.path.exists(writedir1):
        os.makedirs(writedir1)
    if not os.path.exists(writedir2):
        os.makedirs(writedir2)
    if not os.path.exists(writedir4):
        os.makedirs(writedir4)
    if not os.path.exists(writedir8):
        os.makedirs(writedir8)
    Nloops = len(os.listdir(filedir2))
    for i in range(Nloops):
        print('File: %05d' % i)
        filename1 = filedir1 + 'D3--waveforms--%05d.txt' % i
        filename2 = filedir2 + 'D3--waveforms--%05d.txt' % i
        filename4 = filedir4 + 'D3--waveforms--%05d.txt' % i
        filename8 = filedir8 + 'D3--waveforms--%05d.txt' % i
        writename1 = writedir1 + 'D3--waveforms--%05d.txt' % i
        writename2 = writedir2 + 'D3--waveforms--%05d.txt' % i
        writename4 = writedir4 + 'D3--waveforms--%05d.txt' % i
        writename8 = writedir8 + 'D3--waveforms--%05d.txt' % i
        (t1,v1,header1) = rw(filename1,numhead)
        (t2,v2,header2) = rw(filename2,numhead)
        (t4,v4,header4) = rw(filename4,numhead)
        (t8,v8,header8) = rw(filename8,numhead)
        (t_down_1,v_down_1) = downsampling(t1,v1,fsps,new_fsps)
        (t_down_2,v_down_2) = downsampling(t2,v2,fsps,new_fsps)
        (t_down_4,v_down_4) = downsampling(t4,v4,fsps,new_fsps)
        (t_down_8,v_down_8) = downsampling(t8,v8,fsps,new_fsps)
        v_digit_1 = digitize(v_down_1,noise)
        v_digit_2 = digitize(v_down_2,noise)
        v_digit_4 = digitize(v_down_4,noise)
        v_digit_8 = digitize(v_down_8,noise)
        write_waveform(t_down_1,v_digit_1,writename1,header1)
        write_waveform(t_down_2,v_digit_2,writename2,header2)
        write_waveform(t_down_4,v_digit_4,writename4,header4)
        write_waveform(t_down_8,v_digit_8,writename8,header8)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p3",description="Downsamples and digitizes waveform.")
    parser.add_argument("--noise",type=float,help='bits of noise from digitizer',default=3.3)
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--new_fsps",type=float,help="hz, samples/s of new digitizer",default=500000000.0)
    args = parser.parse_args()

    p3(args.noise,args.datadate,args.numhead,args.fsps,args.new_fsps)