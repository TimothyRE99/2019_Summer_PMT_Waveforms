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
def p3(noise_filter,noise,datadate,numhead,fsps,new_fsps,gain_noise,gain_factor_2,gain_factor_4,gain_factor_8,start_index,steps):
    #establishing directory names
    if new_fsps == 1000000000:
        sample_rate = '1 Gsps'
    elif new_fsps == 500000000:
        sample_rate = '500 Msps'
    elif new_fsps == 250000000:
        sample_rate = '250 Msps'
    else:
        sample_rate = 'trash'
    if noise_filter == 0 and gain_noise == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_raw'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_doubled'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_quadrupled'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_octupled'
    elif gain_noise == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_noise=' + str(noise) + 'V'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_raw_noise=' + str(noise_filter) + 'V'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_doubled_noise=' + str(noise_filter) + 'V'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_quadrupled_noise=' + str(noise_filter) + 'V'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_octupled_noise=' + str(noise_filter) + 'V'
    elif noise_filter == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_gain_noise=' + str(gain_noise) + 'V'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_raw_gain_noise=' + str(gain_noise) + 'V'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_doubled_gain_noise=' + str(gain_noise) + 'V'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_octupled_gain_noise=' + str(gain_noise) + 'V'
    else:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_raw_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise_filter) + 'V'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_doubled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise_filter) + 'V'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise_filter) + 'V'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/studies/phase/' + sample_rate + '/phase=' + str(start_index) + '/phase_rise_octupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise_filter) + 'V'
    if gain_factor_2 != 1 or gain_factor_4 != 1 or gain_factor_8:
        filedir1 = filedir1 + '_gained/'
        filedir2 = filedir2 + '_gained/'
        filedir4 = filedir4 + '_gained/'
        filedir8 = filedir8 + '_gained/'
        writedir1 = writedir1 + '_gained_analyzed/'
        writedir2 = writedir2 + '_gained_analyzed/'
        writedir4 = writedir4 + '_gained_analyzed/'
        writedir8 = writedir8 + '_gained_analyzed/'
    else:
        filedir1 = filedir1 + '/'
        filedir2 = filedir2 + '/'
        filedir4 = filedir4 + '/'
        filedir8 = filedir8 + '/'
        writedir1 = writedir1 + '_analyzed/'
        writedir2 = writedir2 + '_analyzed/'
        writedir4 = writedir4 + '_analyzed/'
        writedir8 = writedir8 + '_analyzed/'
    #creating directories if they don't exist
    if not os.path.exists(writedir1):
        os.makedirs(writedir1)
    if not os.path.exists(writedir2):
        os.makedirs(writedir2)
    if not os.path.exists(writedir4):
        os.makedirs(writedir4)
    if not os.path.exists(writedir8):
        os.makedirs(writedir8)
    Nloops = len(os.listdir(filedir2))      #establishing how many files to cycle through
    for i in range(Nloops):
        print('%s/%s, File: %05d' % (start_index + 1,steps,i))             #printing number of file currently being processed
        #establishing read and write names
        filename1 = filedir1 + 'D2--waveforms--%05d.txt' % i
        filename2 = filedir2 + 'D2--waveforms--%05d.txt' % i
        filename4 = filedir4 + 'D2--waveforms--%05d.txt' % i
        filename8 = filedir8 + 'D2--waveforms--%05d.txt' % i
        writename1 = writedir1 + 'Phase--waveforms--%05d.txt' % i
        writename2 = writedir2 + 'Phase--waveforms--%05d.txt' % i
        writename4 = writedir4 + 'Phase--waveforms--%05d.txt' % i
        writename8 = writedir8 + 'Phase--waveforms--%05d.txt' % i
        #reading in waveform values
        (t1,v1,header1) = rw(filename1,numhead)
        (t2,v2,header2) = rw(filename2,numhead)
        (t4,v4,header4) = rw(filename4,numhead)
        (t8,v8,header8) = rw(filename8,numhead)
        #downsampling waveform values
        (t_down_1,v_down_1) = downsampling(t1,v1,fsps,new_fsps,start_index)
        (t_down_2,v_down_2) = downsampling(t2,v2,fsps,new_fsps,start_index)
        (t_down_4,v_down_4) = downsampling(t4,v4,fsps,new_fsps,start_index)
        (t_down_8,v_down_8) = downsampling(t8,v8,fsps,new_fsps,start_index)
        #digitizing waveform values
        v_digit_1 = digitize(v_down_1,noise)
        v_digit_2 = digitize(v_down_2,noise)
        v_digit_4 = digitize(v_down_4,noise)
        v_digit_8 = digitize(v_down_8,noise)
        #saving downsampled and digitized waveforms
        write_waveform(t_down_1,v_digit_1,writename1,header1)
        write_waveform(t_down_2,v_digit_2,writename2,header2)
        write_waveform(t_down_4,v_digit_4,writename4,header4)
        write_waveform(t_down_8,v_digit_8,writename8,header8)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p3",description="Downsamples and digitizes waveform.")
    parser.add_argument("--noise_filter",type=float,help='bits of noise from filter',default=0)
    parser.add_argument("--noise",type=float,help='bits of noise from digitizer',default=3.3)
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--gain_noise",type=float,help="standard deviation of noise gaussian for gain step",default=0)
    parser.add_argument("--gain_factor_2",type=float,help="Factor to multiply doubled by",default=2.9702411538)
    parser.add_argument("--gain_factor_4",type=float,help="Factor to multiply quadrupled by",default=3.9455513908)
    parser.add_argument("--gain_factor_8",type=float,help="Factor to multiply octupled by",default=7.3329373547)
    args = parser.parse_args()

    new_fsps = np.array([1000000000,500000000,250000000])
    for i in range(len(new_fsps)):
        steps = int(args.fsps/new_fsps[i] + 0.5)
        for j in range(steps):
            start_index = j
            p3(args.noise_filter,args.noise,args.datadate,args.numhead,args.fsps,new_fsps[i],args.gain_noise,args.gain_factor_2,args.gain_factor_4,args.gain_factor_8,start_index,steps)