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

def zc_locator(t,v):
    stop_ind = int(len(v)/3)
    v_norm = v/max(v[0:stop_ind])     #normalizes for easy checking
    #creates array of "True" and "False" entries for where condition is met
    checkPeak = v_norm == 1
    checkCross = v_norm <= 0
    #turns into array of indices each value held above
    indexPeak = np.asarray([k for k, x in enumerate(checkPeak) if x])
    indexCross = np.asarray([k for k, x in enumerate(checkCross) if x])
    index_Peak = indexPeak[0]       #creates peak index into int
    #establishes first crossed index after peak
    indexCross_removed = indexCross[np.where(indexCross > index_Peak)]
    index_Cross = indexCross_removed[0]
    #interpolates time of crossing
    t_bef = t[index_Cross - 1]
    t_aft = t[index_Cross]
    v_bef = v[index_Cross - 1]
    v_aft = v[index_Cross]
    slope = (v_aft - v_bef) / (t_aft - t_bef)
    t_pass = (-1 * v_bef) / slope
    t_cross = t_bef + t_pass
    return (t_cross,index_Cross,index_Peak)

#digitizing
def digitize(v,noise):
    v_new = np.array([])
    for i in range(len(v)):
        v_new = np.append(v_new,(v[i] * (2**14 - 1)*2 + 0.5))           #multiplying by digitizer formula to convert to bits
    if noise != 0:
        noise_array = np.random.normal(loc=0.0, scale = noise, size = len(v_new))       #generating noise array
        v_final = np.add(v_new, noise_array)    #adding noise to digitized values
    else:
        v_final = v_new
    v_final = v_final.astype(int)           #converting values to ints
    return(v_final)

#reading and writing waveforms and calling other functions
def p3(new_fsps,datadate,numhead,scale,phase_array,n_box,n_delay,n_att,num_phases):
    filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt'
    t,v,_ = rw(filename,numhead)
    uspl = us(t,v)
    t_cross_array = []
    for i in range(len(phase_array)):
        start_value = t[0] + i/(new_fsps*num_phases)
        end_value = t[-1]
        t_array = np.arange(start_value,end_value,1/new_fsps)
        v_array = -1*uspl(t_array)
        t_array = t_array - i/(new_fsps*num_phases)
        scale_height = scale/np.max(v_array)
        v_scaled = v_array*scale_height
        v_digit = digitize(v_scaled,0)
        t_avg,v_avg = boxcar_wf(t_array,v_digit,n_box)
        v_delay = delay_wf(v_avg,n_delay)
        v_att = attenuate_wf(v_avg,n_att)
        v_sum = sum_wf(v_att,v_delay)
        t_cross,_,_ = zc_locator(t_avg,v_sum)
        t_cross_array.append(t_cross)
    t_cross_init = t_cross_array[0]
    t_cross_array = t_cross_array - t_cross_init
    t_cross_array = np.flip(np.asarray(t_cross_array))
    true_timing_array = np.flip(np.zeros(num_phases) - phase_array)

    fig = plt.gcf()
    fig.show()
    plt.get_current_fig_manager().window.showMaximized()
    fig.canvas.draw()

    for i in range(len(true_timing_array)):
        start_value = t[0] + i/(new_fsps*num_phases)
        t_array = np.arange(start_value,end_value,1/new_fsps)
        v_array = -1*uspl(t_array)
        t_array = t_array - i/(new_fsps*num_phases)
        scale_height = scale/np.max(v_array)
        v_scaled = v_array*scale_height
        v_digit = digitize(v_scaled,0)
        t_avg,v_avg = boxcar_wf(t_array,v_digit,n_box)
        t_avg = t_avg - t_cross_init
        v_delay = delay_wf(v_avg,n_delay)
        v_att = attenuate_wf(v_avg,n_att)
        v_sum = sum_wf(v_att,v_delay)
        t_cross,index_Cross,index_Peak = zc_locator(t_avg,v_sum)
        plt.clf()
        plt.subplot(1,2,1)
        plt.plot(t_avg,v_sum)
        plt.plot(t_avg,v_delay,color = 'green')
        plt.plot(t_avg,v_att,color='purple')
        plt.scatter(t_avg,v_sum)
        plt.scatter(t_avg,v_delay,color = 'green')
        plt.scatter(t_avg,v_att,color='purple')
        plt.axhline(0,color='black')
        plt.axvline(t_cross,color='red')
        plt.axvline(true_timing_array[-1*i],color='black')
        plt.plot(t_avg[index_Cross],v_sum[index_Cross],'x',color = 'orange')
        plt.plot(t_avg[index_Peak],v_sum[index_Peak],'x',color = 'yellow')
        plt.subplot(1,2,2)
        true_timing_value = true_timing_array[-1*i]
        plt.plot(true_timing_array,t_cross_array)
        plt.axvline(true_timing_value,color='Black')
        plt.pause(0.01)
        fig.canvas.draw()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="spline unnoised animate",description="Runs animation of splined waveform along timing and CFD for comparison.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    args = parser.parse_args()

    new_fsps = 250000000
    num_phases = 160
    phase_array = np.linspace(0,1/new_fsps,num_phases,endpoint=False)
    scale = .0065313
    p3(new_fsps,args.datadate,args.numhead,scale,phase_array,2,1,2,num_phases)