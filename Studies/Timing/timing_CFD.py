#runs files through CFD algorithm for timing study use

#import necessary
import os
import numpy as np
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#runs boxcar averaging algorithm
def boxcar_wf(t,v,n):
    if(n==0): 
        return t,v
    v1 = np.zeros(len(v)-n)
    t1 = np.zeros(len(t)-n)
    for i in range(len(v1)): 
        vsum = 0
        for j in range(n):
            vsum += v[n+i-j]
        v1[i]=float(vsum)/float(n)
        t1[i] = t[i] 
    return t1,v1

#runs inversion and shift of waveform
def shift_wf(v,n):
    v1 = -1 * v
    if n == 0:
        return v1
    v1_insert = np.zeros(n)
    v1 = np.insert(v1,0,v1_insert)[:-n]
    return v1

#runs multiplication of other waveform
def multiply_wf(v,n):
    if n == 1:
        return v
    v1 = v * n
    return v1

#sums waveforms together
def sum_wf(v_mult,v_shift):
    v_sum = np.add(v_mult,v_shift)
    return v_sum

#calls other functions
def timing_CFD(datadate,numhead,subfolder,n_box,n_shift,n_mult):
    writedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/nshift='+str(n_shift)+'/nmult='+str(n_mult)+'/'+subfolder+'/'
    if not os.path.exists(writedir):
        os.makedirs(writedir)
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'
    Nloops = len(os.listdir(filedir))
    for i in range(Nloops):
        print("File: %05d" % i)
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        writename = writedir + 'D3--waveforms--%05d.txt' % i
        (t,v,header) = rw(filename,numhead)
        t_avg,v_avg = boxcar_wf(t,v,n_box)
        v_shift = shift_wf(v_avg,n_shift)
        v_mult = multiply_wf(v_avg,n_mult)
        v_sum = sum_wf(v_mult,v_shift)
        write_waveform(t_avg,v_sum,writename,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="timing CFD",description="Applies CFD algorithm to prepare for ZCF.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw')
    parser.add_argument('--n_box',type=int,help='n value for boxcar averager',default = 4)
    parser.add_argument('--n_shift',type=int,help='number of indices to shift inverted waveform',default = 1)
    parser.add_argument('--n_mult',type=int,help='amount to multiply base waveform by, must be power of 2',default = 1)
    args = parser.parse_args()

    timing_CFD(args.datadate,args.numhead,args.subfolder,args.n_box,args.n_shift,args.n_mult)