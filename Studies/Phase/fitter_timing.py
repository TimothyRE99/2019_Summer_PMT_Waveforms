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

def horiz_align(t,v,t_fitter,v_fitter,i):
    return(t_fitter - i*1/20000000000)

def scale_determine(t,v,t_fitter,v_fitter,offset):
    v_max = np.amax(v)
    index_2 = np.where(v == v_max)[0][0]
    index = index_2 + offset
    t_1 = t[index]
    index_fitter_find_array = np.abs(t_fitter - t_1)
    index_fitter = np.where(index_fitter_find_array == np.amin(index_fitter_find_array))[0]
    scale = v[index]/v_fitter[index_fitter]
    return(scale)

def timing_extraction(t_fitter,v_fitter):
    v_fitter_max = np.amax(v_fitter)
    v_fitter_max_index = np.where(v_fitter == v_fitter_max)[0][0]
    v_fitter = v_fitter[0:v_fitter_max_index]
    v_fitter_zero = v_fitter_max/2
    v_fitter_zero_array = np.abs(v_fitter - v_fitter_zero)
    v_fitter_zero_index = np.where(v_fitter_zero_array == np.amin(v_fitter_zero_array))[0]
    t_cross = t_fitter[v_fitter_zero_index]
    return(t_cross)

def fitter_timing(datadate,numhead,samplerate,samplerate_name,shaping):
    if samplerate_name == 'INVALID':
        return("Failed")
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)

    difference_list = []
    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name
    Nloops = len(os.listdir(filedir + '/phase=0/phase_'+shaping+'/'))
    for j in range(Nloops):
        scale_array = []
        print(j)
        i = random.randint(0,maxphase - 1)
        t_fitter,v_fitter,_ = rw('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt',1)
        filename = filedir + '/phase='+str(i)+'/phase_'+shaping+'/Phase--waveforms--%05d.txt' % j
        (t,v,_) = rw(filename,numhead)
        v = -1*v
        t_fitter = horiz_align(t,v,t_fitter,v_fitter,i)
        scale_1 = scale_determine(t,v,t_fitter,v_fitter,-1)
        scale_2 = scale_determine(t,v,t_fitter,v_fitter,0)
        scale_3 = scale_determine(t,v,t_fitter,v_fitter,1)
        scale_array.append(scale_1)
        scale_array.append(scale_2)
        scale_array.append(scale_3)
        scale = 0
        num_ignore = 0
        for k in scale_array:
            if k < 0:
                num_ignore += 1
            else:
                scale += k
        scale = scale/(len(scale_array) - num_ignore)
        v_fitter = v_fitter*scale
        t_cross = timing_extraction(t_fitter, v_fitter)
        difference_list.append(-1*i*phase_time - t_cross)
        if difference_list[j] < -1e-9 or difference_list[j] > 1e-9:
            plt.plot(t,v)
            plt.scatter(t,v)
            plt.plot(t_fitter,v_fitter)
            plt.scatter(t_fitter,v_fitter)
            plt.axvline(t_cross,color = 'Red')
            plt.axvline(-1*i*phase_time,color = 'Black')
            plt.title(str(j))
            plt.show()

    difference_list = np.asarray(difference_list)
    median_value = np.median(difference_list)
    difference_list -= median_value

    true_mean = '%5g' % np.mean(difference_list)
    true_std = '%5g' % np.std(difference_list)
    histo_data, bins_data = np.histogram(difference_list, bins = 200)
    binwidth = (bins_data[1] - bins_data[0])                    #determining bin width
    #determining bin centers
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    plt.rcParams.update({'font.size': 14})
    plt.bar(binscenters, histo_data, width=binwidth)        #plotting histogram
    plt.xlabel('True Timing - Recovered Timing')
    plt.ylabel('Count')
    plt.title('Corrected Timings\nGaussian Fite Values:\nMean = '+true_mean+' seconds\nStandard Deviation ='+true_std+' seconds')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()

    return("Passed")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="fitter timing",description="Uses average waveform to fit for timing")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
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