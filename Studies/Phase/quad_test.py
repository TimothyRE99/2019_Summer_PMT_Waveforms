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
def mult_wf(v,n):
    #doesn't attenuate if n = 1
    if n == 1:
        return v
    #divides by n otherwise
    v = v * n
    return v

#sums waveforms together
def sum_wf(v_mult,v_avg):
    v_sum = np.add(v_mult,-1*v_avg)       #adds waveforms together
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
    index_2 = indexCross_removed[0]
    #interpolates time of crossing
    index_1 = index_2 - 1
    index_3 = index_2 + 1
    if (v[index_1] - v[index_2]) > (v[index_2] - v[index_3]):
        index_1 = index_1  -  1
        index_2 = index_2  -  1
        index_3 = index_3  -  1
    x1 = t[index_1]
    x2 = t[index_2]
    x3 = t[index_3]
    y1 = v[index_1]
    y2 = v[index_2]
    y3 = v[index_3]
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    a = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    b = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    c = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom
    d = b**2-4*a*c
    cross_1 = (-b + math.sqrt(d))/(2*a)
    cross_2 = (-b - math.sqrt(d))/(2*a)
    if x1 < cross_1 < x3:
        t_cross = cross_1
    else:
        t_cross = cross_2
    return (t_cross,index_1,index_2,index_3)

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
        v_mult = mult_wf(v_delay,n_att)
        v_sum = sum_wf(v_mult,v_avg)
        t_cross,_,_,_ = zc_locator(t_avg,v_sum)
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
        v_mult = mult_wf(v_delay,n_att)
        v_sum = sum_wf(v_mult,v_avg)
        t_cross,index_1,index_2,index_3  = zc_locator(t_avg,v_sum)
        plt.clf()
        plt.subplot(1,2,1)
        plt.plot(t_avg,v_sum)
        plt.plot(t_avg,v_mult,color = 'green')
        plt.plot(t_avg,-1*v_avg,color='purple')
        plt.scatter(t_avg,v_sum)
        plt.scatter(t_avg,v_mult,color = 'green')
        plt.scatter(t_avg,-1*v_avg,color='purple')
        plt.axhline(0,color='black')
        plt.axvline(t_cross,color='red')
        plt.axvline(true_timing_array[-1*i],color='black')
        plt.plot(t_avg[index_1],v_sum[index_1],'x',color = 'orange')
        plt.plot(t_avg[index_2],v_sum[index_2],'x',color = 'yellow')
        plt.plot(t_avg[index_3],v_sum[index_3],'x',color = 'magenta')
        plt.subplot(1,2,2)
        true_timing_value = true_timing_array[-1*i]
        plt.plot(true_timing_array,t_cross_array)
        plt.axvline(true_timing_value,color='Black')
        plt.title(str(i))
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