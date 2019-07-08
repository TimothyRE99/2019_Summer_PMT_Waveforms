#Calculates charge for waveform and corresponding downsampled and digitized waveform and compares

#import necessary
import os
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh

#calculates charge
def charge_det(t,v):
    area = 0
    for i in range(len(v)-1):
        area += ((t[i+1]-t[i]) * v[i])
    charge = str(-1*area/50)
    return(charge)

#converting standard waveform to digitized, no noise, no donwsampling
def digitize(v):
    v_new = np.array([])
    for i in range(len(v)):
        v_new = np.append(v_new,(v[i] * (2**14 - 1)*2 + 0.5))
    v_final = v_new.astype(int)
    return(v_final)

#calling functions
def charge_compare(datadate,numhead,subfolder):
    writedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/charge/'
    if not os.path.exists(writedir):
        os.makedirs(writedir)
    writename = writedir + subfolder + '_normal_charge.txt'
    writename_digitized = writedir + subfolder + '_digitized_charge.txt'
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'/'
    filedir_digitized = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'
    Nloops = len(os.listdir(filedir_digitized))
    for i in range(Nloops):
        print('Filename: %05d' % i)
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        filename_digitized = filedir_digitized + 'D3--waveforms--%05d.txt' % i
        (t,v,_) = rw(filename,numhead)
        (t_digit,v_digit,_) = rw(filename_digitized,numhead)
        v = digitize(v)
        charge = charge_det(t,v)
        charge_digit = charge_det(t_digit,v_digit)
        wh(charge,writename)
        wh(charge_digit,writename_digitized)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="charge_compare",description="Compares charge for original waveform and digitized waveform.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw_gained')
    args = parser.parse_args()

    charge_compare(args.datadate,args.numhead,args.subfolder)