import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os
import random
import math
from readwaveform import read_waveform as rw
from writewaveform import write_waveform as ww
import scipy.interpolate as it
from unispline import unispline as us

def fitter_timing(datadate,numhead,samplerate,samplerate_name,shaping):
    if samplerate_name == 'INVALID':
        return("Failed")
    numhead = 5
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    phase_array = np.arange(0,maxphase)
    for i in phase_array:
        t_fitter,v_fitter,_ = rw('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt',1)
        t_fitter -= i*1/20000000000
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase='+str(i)+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        for j in range(Nloops):
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            v = -1*v
            v_max = np.amax(v)
            index_2 = np.where(v == v_max)[0]
            index_1 = index_2 - 1
            t_1 = t[index_1]
            t_2 = t[index_2]
            index_fitter_1_find_array = np.abs(t_fitter - t_1)
            index_fitter_2_find_array = np.abs(t_fitter - t_2)
            index_fitter_1 = np.where(index_fitter_1_find_array == np.amin(index_fitter_1_find_array))[0]
            index_fitter_2 = np.where(index_fitter_2_find_array == np.amin(index_fitter_2_find_array))[0]
            scale_1 = v[index_1]/v_fitter[index_fitter_1]
            scale_2 = v[index_2]/v_fitter[index_fitter_2]
            scale = (scale_1 + scale_2)/2
            v_fitter = v_fitter*scale
            plt.plot(t,v)
            plt.scatter(t,v)
            plt.plot(t_fitter,v_fitter)
            plt.scatter(t_fitter,v_fitter)
            plt.get_current_fig_manager().window.showMaximized()
            plt.show()

    return("Passed")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="fitter timing",description="Uses average waveform to fit for timing")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument('--samplerate',type=int,help='samples per second',default = 250000000)
    parser.add_argument('--shaping',type=str,help='name of shaping',default = 'raw_gained_analyzed')
    args = parser.parse_args()

    if args.samplerate == 250000000:
        samplerate_name = '250 Msps'
    elif args.samplerate == 500000000:
        samplerate_name = '500 Msps'
    elif args.samplerate == 1000000000:
        samplerate_name = '1 Gsps'
    else:
        samplerate_name = 'INVALID'
    
    status = fitter_timing(args.datadate,args.numhead,args.samplerate,samplerate_name,args.shaping)
    print(status)