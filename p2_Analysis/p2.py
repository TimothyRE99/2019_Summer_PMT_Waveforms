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

#applying lowpass filter and writing
def p2(datadate,numhead,fsps,x_values,noise):
    #establish tau values from average waveform
    tau_double = 2.18e-8
    tau_quadruple = 1.13e-8
    tau_octuple = 4.15e-8
    #establish directories for reading and writing waveforms
    filedir = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/'
    if noise == 0:
        writedir_two = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled/'
        writedir_four = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled/'
        writedir_eight = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled/'
    else:
        writedir_two = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V/'
        writedir_four = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V/'
        writedir_eight = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V/'
    #creating write directories if they're not there
    if not os.path.exists(writedir_two):
        os.makedirs(writedir_two)
    if not os.path.exists(writedir_four):
        os.makedirs(writedir_four)
    if not os.path.exists(writedir_eight):
        os.makedirs(writedir_eight)
    #establishing length of raw directory and subtracting one due to info file
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw')) - 1
    #cycling through all waveform files in directory
    for i in range(Nloops):
        print("File: %05d" % i)
        #establishing file names for reading and writing
        filename = filedir + 'D2--waveforms--%05d.txt' % i
        writename_two = writedir_two + 'D2--waveforms--%05d.txt' % i
        writename_four = writedir_four + 'D2--waveforms--%05d.txt' % i
        writename_eight = writedir_eight + 'D2--waveforms--%05d.txt' % i
        #calculating and writing double files
        (t,v,header) = rw(filename,numhead)
        v_taued = lpf(v,tau_double,fsps)
        if noise != 0:
            v_taued = noise_add(v_taued,noise)
        write_waveform(t,v_taued,writename_two,header)
        #calculating and writing quadruple files
        (t,v,header) = rw(writename_two,numhead)
        v_taued = lpf(v,tau_quadruple,fsps)
        if noise != 0:
            v_taued = noise_add(v_taued,noise)
        write_waveform(t,v_taued,writename_four,header)
        #calculating and writing octuple files
        (t,v,header) = rw(writename_four,numhead)
        v_taued = lpf(v,tau_octuple,fsps)
        if noise != 0:
            v_taued = noise_add(v_taued,noise)
        write_waveform(t,v_taued,writename_eight,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2",description="Runs lowpass program on waveforms to increase rise time by appropriate amount")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--x_values",type=int,help="number of taus to generate",default=5000)
    parser.add_argument("--noise",type=float,help="standard deviation of noise gaussian",default=0.0002)
    args = parser.parse_args()

    p2(args.datadate,args.numhead,args.fsps,args.x_values,args.noise)