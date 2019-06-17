#take in waveform and apply low pass filters for 2, 4, and 8 times 10-90 rise time

#import necessary
import numpy as np
import os
from p2_lowpass import lpfFirstOrder as lpf
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import shutil

#applying noise to waveform
def noise_add(v,noise):
    noise_array = np.random.normal(loc=0.0, scale = noise, size = len(v))
    v_final = np.add(v, noise_array)
    return(v_final)

#applying gain and gain noise
def gain(v,gain_noise,gain_factor):
    v_intermed = v * gain_factor
    if gain_noise != 0:
        v_final = noise_add(v_intermed,gain_noise)
    else:
        v_final = v_intermed
    return v_final

#applying lowpass filter and writing
def p2(datadate,numhead,fsps,x_values,noise,gain_noise,gain_factor_2,gain_factor_4,gain_factor_8):
    #establish tau values from average waveform
    tau_double = 2.18e-8
    tau_quadruple = 1.13e-8
    tau_octuple = 4.15e-8
    #establish directories for reading and writing waveforms
    filedir = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/'
    if noise == 0 and gain_noise == 0:
        writedir_1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw'
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled'
    elif gain_noise == 0:
        writedir_1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_doubled_noise=' + str(noise) + 'V'
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V'
    elif noise == 0:
        writedir_1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_gain_noise=' + str(gain_noise) + 'V'
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V'
    else:
        writedir_1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
    if gain_factor_2 != 1 or gain_factor_4 != 1 or gain_factor_8:
        writedir_1 = writedir_1 + '_gained/'
        writedir_2 = writedir_2 + '_gained/'
        writedir_4 = writedir_4 + '_gained/'
        writedir_8 = writedir_8 + '_gained/'
    else:
        writedir_1 = writedir_1 + '/'
        writedir_2 = writedir_2 + '/'
        writedir_4 = writedir_4 + '/'
        writedir_8 = writedir_8 + '/'
    #creating write directories if they're not there
    if not os.path.exists(writedir_1):
        os.makedirs(writedir_1)
    if not os.path.exists(writedir_2):
        os.makedirs(writedir_2)
    if not os.path.exists(writedir_4):
        os.makedirs(writedir_4)
    if not os.path.exists(writedir_8):
        os.makedirs(writedir_8)
    #establishing length of raw directory and subtracting one due to info file
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw')) - 1
    #cycling through all waveform files in directory
    for i in range(Nloops):
        print("File: %05d" % i)
        #establishing file names for reading and writing
        filename = filedir + 'D2--waveforms--%05d.txt' % i
        writename_1 = writedir_1 + 'D2--waveforms--%05d.txt' % i
        writename_2 = writedir_2 + 'D2--waveforms--%05d.txt' % i
        writename_4 = writedir_4 + 'D2--waveforms--%05d.txt' % i
        writename_8 = writedir_8 + 'D2--waveforms--%05d.txt' % i
        #calculating and writing double files
        (t,v_2,header) = rw(filename,numhead)
        v_taued_2 = lpf(v_2,tau_double,fsps)
        if noise != 0:
            v_taued_2 = noise_add(v_taued_2,noise)
        #calculating and writing quadruple files
        v_taued_4 = lpf(v_taued_2,tau_quadruple,fsps)
        if noise != 0:
            v_taued_4 = noise_add(v_taued_4,noise)
        #calculating and writing octuple files
        v_taued_8 = lpf(v_taued_4,tau_octuple,fsps)
        if noise != 0:
            v_taued_8 = noise_add(v_taued_8,noise)
        #adding gain to waveforms
        if gain_factor_2 != 1:
            v_taued_2 = gain(v_taued_2,gain_noise,gain_factor_2)
        if gain_factor_4 != 1:
            v_taued_4 = gain(v_taued_4,gain_noise,gain_factor_4)
        if gain_factor_8 != 1:
            v_taued_8 = gain(v_taued_8,gain_noise,gain_factor_8)
        #writing waveforms
        shutil.copy2(filedir + 'd1_info.txt',writename_1)
        shutil.copy2(filename,writename_1)
        write_waveform(t,v_taued_2,writename_2,header)
        write_waveform(t,v_taued_4,writename_4,header)
        write_waveform(t,v_taued_8,writename_8,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2",description="Runs lowpass program on waveforms to increase rise time by appropriate amount")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--x_values",type=int,help="number of taus to generate",default=5000)
    parser.add_argument("--noise",type=float,help="standard deviation of noise gaussian",default=0)
    parser.add_argument("--gain_noise",type=float,help="standard deviation of noise gaussian for gain step",default=0)
    parser.add_argument("--gain_factor_2",type=float,help="Factor to multiply doubled by",default=3.5867418798)
    parser.add_argument("--gain_factor_4",type=float,help="Factor to multiply quadrupled by",default=4.52070370286)
    parser.add_argument("--gain_factor_8",type=float,help="Factor to multiply octupled by",default=8.09019004097)
    args = parser.parse_args()

    p2(args.datadate,args.numhead,args.fsps,args.x_values,args.noise,args.gain_noise,args.gain_factor_2,args.gain_factor_4,args.gain_factor_8)