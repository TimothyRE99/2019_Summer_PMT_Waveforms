#take in waveform and apply low pass filters for 2, 4, and 8 times 10-90 rise time

#import necessary
import numpy as np
import os
from p2_lowpass import lpfFirstOrder as lpf
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#applying lowpass filter and writing
def p2(datadate,numhead,fsps,x_values):
    #establish tau values from average waveform
    tau_double = 2e-8
    tau_quadruple = 2e-8
    tau_octuple = 2e-8
    #establish directories for reading and writing waveforms
    filedir = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/'
    writedir_two = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled/'
    writedir_four = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled/'
    writedir_eight = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled/'
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
        write_waveform(t,v_taued,writename_two,header)
        #calculating and writing quadruple files
        (t,v,header) = rw(writename_two,numhead)
        v_taued = lpf(v,tau_quadruple,fsps)
        write_waveform(t,v_taued,writename_four,header)
        #calculating and writing octuple files
        (t,v,header) = rw(writename_four,numhead)
        v_taued = lpf(v,tau_octuple,fsps)
        write_waveform(t,v_taued,writename_eight,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2",description="Runs lowpass program on waveforms to increase rise time by appropriate amount")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--x_values",type=int,help="number of taus to generate",default=5000)
    args = parser.parse_args()

    p2(args.datadate,args.numhead,args.fsps,args.x_values)