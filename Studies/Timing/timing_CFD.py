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
def delay_wf(v,n):
    if n == 0:
        return v
    v_insert = np.zeros(n)
    v1 = np.insert(v,0,v_insert)[:-n]
    return v1

#runs multiplication of other waveform
def attenuate_wf(v,n):
    v1 = -1 * v
    if n == 1:
        return v
    v1 = v / n
    return v1

#sums waveforms together
def sum_wf(v_att,v_delay):
    v_sum = np.add(v_att,v_delay)
    return v_sum

#calls other functions
def timing_CFD(datadate,numhead,subfolder,n_box,n_delay,n_att):
    writedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/ndelay='+str(n_delay)+'/natt='+str(n_att)+'/'+subfolder+'/'
    if not os.path.exists(writedir):
        os.makedirs(writedir)
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'
    Nloops = len(os.listdir(filedir))
    for i in range(Nloops):
        print("File: %05d, NBOX: " % i + str(n_box) + ", NDELAY:" + str(n_delay) + " , NATT: " + str(n_att))
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        writename = writedir + 'D3--waveforms--%05d.txt' % i
        (t,v,header) = rw(filename,numhead)
        t_avg,v_avg = boxcar_wf(t,v,n_box)
        v_delay = delay_wf(v_avg,n_delay)
        v_att = attenuate_wf(v_avg,n_att)
        v_sum = sum_wf(v_att,v_delay)
        write_waveform(t_avg,v_sum,writename,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="timing CFD",description="Applies CFD algorithm to prepare for ZCF.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'rise_doubled')
    args = parser.parse_args()

    for n_box in range(5):
        if n_box == 3:
            pass
        else:
            for n_delay in range(1,5):
                if n_delay == 3:
                    pass
                else:
                    for n_att in range(1,5):
                        if n_att == 3:
                            pass
                        else:
                            timing_CFD(args.datadate,args.numhead,args.subfolder,n_box,n_delay,n_att)