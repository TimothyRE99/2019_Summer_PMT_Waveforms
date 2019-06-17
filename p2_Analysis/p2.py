#take in waveform and apply low pass filters for 2, 4, and 8 times 10-90 rise time

#import necessary
import numpy as np
import os
from p2_lowpass import lpfFirstOrder as lpf
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#applying noise to waveform
def noise_add(v,noise):
    noise_array = np.random.normal(loc=0.0, scale = noise, size = len(v))
    v_final = np.add(v, noise_array)
    return(v_final)

#applying gain and gain noise
def gain(v,gain_noise,gain_target):
    if gain_target > 0:
        gain_target = -1 * gain_target
    v_inter = v * (gain_target / min(v))
    if gain_noise != 0:
        v_final = noise_add(v_inter,gain_noise)
    return v_final

#applying lowpass filter and writing
def p2(datadate,numhead,fsps,x_values,noise,gain_noise,gain_target):
    #establish tau values from average waveform
    tau_double = 2.18e-8
    tau_quadruple = 1.13e-8
    tau_octuple = 4.15e-8
    #establish directories for reading and writing waveforms
    filedir = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/'
    if noise == 0 and gain_noise == 0:
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled/'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled/'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled/'
    elif gain_noise == 0:
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V/'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V/'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V/'
    elif noise == 0:
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V/'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V/'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V/'
    else:
        writedir_2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V/'
        writedir_4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V/'
        writedir_8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V/'
    #creating write directories if they're not there
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
        writename_2 = writedir_2 + 'D2--waveforms--%05d.txt' % i
        writename_4 = writedir_4 + 'D2--waveforms--%05d.txt' % i
        writename_8 = writedir_8 + 'D2--waveforms--%05d.txt' % i
        #calculating and writing double files
        (t_2,v_2,header_2) = rw(filename,numhead)
        v_taued_2 = lpf(v_2,tau_double,fsps)
        if noise != 0:
            v_taued_2 = noise_add(v_taued_2,noise)
        if gain_target != 0:
            v_taued_2 = gain(v_taued_2,gain_noise,gain_target)
        write_waveform(t_2,v_taued_2,writename_2,header_2)
        #calculating and writing quadruple files
        (t_4,v_4,header_4) = rw(writename_2,numhead)
        v_taued_4 = lpf(v_4,tau_quadruple,fsps)
        if noise != 0:
            v_taued_4 = noise_add(v_taued_4,noise)
        if gain_target != 0:
            v_taued_4 = gain(v_taued_4,gain_noise,gain_target)
        write_waveform(t_4,v_taued_4,writename_4,header_4)
        #calculating and writing octuple files
        (t_8,v_8,header_8) = rw(writename_4,numhead)
        v_taued_8 = lpf(v_8,tau_octuple,fsps)
        if noise != 0:
            v_taued_8 = noise_add(v_taued_8,noise)
        if gain_target != 0:
            v_taued_8 = gain(v_taued_8,gain_noise,gain_target)
        write_waveform(t_8,v_taued_8,writename_8,header_8)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2",description="Runs lowpass program on waveforms to increase rise time by appropriate amount")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--x_values",type=int,help="number of taus to generate",default=5000)
    parser.add_argument("--noise",type=float,help="standard deviation of noise gaussian",default=0)
    parser.add_argument("--gain_noise",type=float,help="standard deviation of noise gaussian for noise step",default=0)
    parser.add_argument("--gain_target",type=float,help="target height/peak value for adding gain",default=0)
    args = parser.parse_args()

    p2(args.datadate,args.numhead,args.fsps,args.x_values,args.noise,args.gain_noise,args.gain_target)