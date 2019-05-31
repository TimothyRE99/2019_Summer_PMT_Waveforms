#take in waveform and apply low pass filters for 2, 4, and 8 times 10-90 rise time

#import necessary
import numpy as np
import os
from p2_lowpass import lpfFirstOrder as lpf
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#applying lowpass filter and writing
def p2(datadate,numhead,fsps):
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
        #establishing file names for reading and writing
        filename = filedir + 'D2--waveforms--%05d.txt' % i
        writename_two = writedir_two + 'D2--waveforms--%05d.txt' % i
        writename_four = writedir_four + 'D2--waveforms--%05d.txt' % i
        writename_eight = writedir_eight + 'D2--waveforms--%05d.txt' % i
        (t,v,header) = rw(filename,numhead)         #taking in information from waveform
        #setting taus based on value necessary to double, quadruple, and octuple rise time
        tau_two = 0.000000005
        tau_four = 0.000000005
        tau_eight = 0.000000005
        #running low pass filter for each tau
        y_two = lpf(v,tau_two,fsps)
        y_four = lpf(v,tau_four,fsps)
        y_eight = lpf(v,tau_eight,fsps)
        #writing results of each lpf to proper location
        write_waveform(t,y_two,writename_two,header)
        write_waveform(t,y_four,writename_four,header)
        write_waveform(t,y_eight,writename_eight,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2",description="Runs lowpass program on waveforms to increase rise time by appropriate amount")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    args = parser.parse_args()

    p2(args.datadate,args.numhead,args.fsps)