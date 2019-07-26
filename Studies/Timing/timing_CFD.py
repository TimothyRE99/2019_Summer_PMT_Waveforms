#runs files through CFD algorithm for timing study use

#import necessary
import os
import numpy as np
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#runs boxcar averaging algorithm
def boxcar_wf(t,v,n):
    if(n==0):       #returns standard values if n = 0
        return t,v
    #reduces length of array by n if n > 0
    v1 = np.zeros(len(v)-n)
    t1 = np.zeros(len(t)-n)
    #runs boxcar moving average on array
    for i in range(len(v1)): 
        vsum = 0
        for j in range(n):
            vsum += v[n+i-j]
        v1[i]=float(vsum)/float(n)
        t1[i] = t[i] 
    return t1,v1

#runs delay of waveform
def delay_wf(v,n):
    #pads beginning of array with n 0's and removes n final indices
    v_insert = np.zeros(n)
    v1 = np.insert(v,0,v_insert)[:-n]
    return v1

#runs inversion and attenuation of waveform
def attenuate_wf(v,n):
    v1 = -1 * v     #inverts waveform
    #doesn't attenuate if n = 1
    if n == 1:
        return v1
    #divides by n otherwise
    v1 = v1 / n
    return v1

#sums waveforms together
def sum_wf(v_att,v_delay):
    v_sum = np.add(v_att,v_delay)       #adds waveforms together
    return v_sum

#calls other functions
def timing_CFD(datadate,numhead,subfolder,n_box,n_delay,n_att,samplerate):
    #establishes directory to write to
    writedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/' + samplerate + 'nbox='+str(n_box)+'/ndelay='+str(n_delay)+'/natt='+str(n_att)+'/'+subfolder+'/'
    #creates write directory if needed
    if not os.path.exists(writedir):
        os.makedirs(writedir)
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/' + samplerate + '/d3_' + subfolder + '_analyzed/'        #says what directory to read from
    Nloops = len(os.listdir(filedir))       #establishes number of files to cylce through
    for i in range(Nloops):
        print("File: %05d, NBOX: " % i + str(n_box) + ", NDELAY: " + str(n_delay) + " , NATT: " + str(n_att))
        #establishes file to read from and write to
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        writename = writedir + 'D3--waveforms--%05d.txt' % i
        (t,v,header) = rw(filename,numhead)     #reads in file
        #applies CFD algorithm
        t_avg,v_avg = boxcar_wf(t,v,n_box)
        v_delay = delay_wf(v_avg,n_delay)
        v_att = attenuate_wf(v_avg,n_att)
        v_sum = sum_wf(v_att,v_delay)
        write_waveform(t_avg,v_sum,writename,header)    #writes waveform to file

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="timing CFD",description="Applies CFD algorithm to prepare for ZCF.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw_gained')
    parser.add_argument('--samplerate',type = str,help = 'downsampled rate to analyze (1 Gsps, 500 Msps, 250 Msps, 125 Msps)',default = '1 Gsps')
    args = parser.parse_args()

    #cycles through each combination of n values
    #for n_box in range(5):
    #    if n_box == 3:
    #        pass
    #    else:
    #        for n_delay in range(1,17):
    #            if n_delay != 1 and n_delay != 2 and n_delay != 4 and n_delay != 8 and n_delay !=  16:
    #                pass
    #            else:
    #                for n_att in range(1,5):
    #                    if n_att == 3:
    #                        pass
    #                    else:
    #                        timing_CFD(args.datadate,args.numhead,args.subfolder,n_box,n_delay,n_att,args.samplerate)
    timing_CFD(args.datadate,args.numhead,args.subfolder,2,1,2,args.samplerate)