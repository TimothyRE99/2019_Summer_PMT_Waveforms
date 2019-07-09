#Calculates charge for waveform and corresponding downsampled and digitized waveform

#import necessary
import os
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from gausshistogram import gauss_histogram as gh
from readhistogram import read_histogram as rh

#calculates charge
def charge_det(t,v,sumtype):
    area = 0        #initialize area
    #calculate charge
    for i in range(len(v)-1):
        if sumtype == 'left':
            area += ((t[i+1]-t[i]) * v[i])
        elif sumtype == 'right':
            area += ((t[i+1]-t[i]) * v[i+1])
        else:
            area += ((t[i+1]-t[i]) * (v[i]+v[i+1])/2)
    charge = str(-1*area/50)
    return(charge)

#converting standard waveform to digitized, no noise, no donwsampling
def digitize(v):
    v_new = np.array([])        #initialize array
    #run digitization formula
    for i in range(len(v)):
        v_new = np.append(v_new,(v[i] * (2**14 - 1)*2 + 0.5))
    v_final = v_new.astype(int)
    return(v_final)

#calling functions
def charge_calc(datadate,numhead,subfolder,sumtype):
    writedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/charge/' + sumtype + '/' #establish name of directory to write data to
    #creating directory if it doesn't exist
    if not os.path.exists(writedir):
        os.makedirs(writedir)
    #establishing names of directory to read files from and txt file to write files to
    writename = writedir + subfolder + '_normal_charge.txt'
    writename_digitized = writedir + subfolder + '_digitized_charge.txt'
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'/'
    filedir_digitized = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'
    Nloops = len(os.listdir(filedir_digitized))     #establish number of files to cycle through
    for i in range(Nloops):
        print('Filename: %05d' % i)
        #establishing txt file names to read from
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        filename_digitized = filedir_digitized + 'D3--waveforms--%05d.txt' % i
        #read in t and v data from files
        (t,v,_) = rw(filename,numhead)
        (t_digit,v_digit,_) = rw(filename_digitized,numhead)
        v = digitize(v)         #digitize original, not-downsampled file
        #calculate charges
        charge = charge_det(t,v,sumtype)
        charge_digit = charge_det(t_digit,v_digit,sumtype)
        #write charges to histogram files
        wh(charge,writename)
        wh(charge_digit,writename_digitized)
    (histo_mean,histo_std) = gh(writename)
    (histo_mean_digitized,histo_std_digitized) = gh(writename_digitized)
    savename = subfolder + '_' + sumtype
    savename_digitized = subfolder + '_' + sumtype + '_digitized'
    rh(writename,"Bits*s / Ohm","Histogram of Charge",savename,datadate,histo_mean,histo_std)
    rh(writename_digitized,"Bits*s / Ohm","Histogram of Charge",savename_digitized,datadate,histo_mean_digitized,histo_std_digitized)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="charge calc",description="Calculates charge for original waveform digitized and digitized waveform with noise in bit*s/ohm.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw_gained')
    parser.add_argument('--sumtype',type = str,help = 'left or right rectangles or trapezoids (must be "left" or "right" or "trap")',default = 'left')
    args = parser.parse_args()

    #defaulting sumtype to left if the input is improper
    if args.sumtype == 'left' or args.sumtype == 'right' or args.sumtype == 'trap':
        sumtype = args.sumtype
    else:
        print("Improper Sumtype, defaulting to Left Rectangles")
        sumtype = 'left'

    charge_calc(args.datadate,args.numhead,args.subfolder,sumtype)