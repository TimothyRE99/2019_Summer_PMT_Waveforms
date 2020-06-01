#import necessary
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from readwaveform import read_waveform as rw
import random
from scipy.optimize import curve_fit as cf

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

def plot_waveform(datadate,numhead,shaping,n_box,n_delay,n_att,samplerate_name):
    phase_time = 1/20000000000
    phase_array = np.array([0,41])
    median_array = []
    correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/averages_splined/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        y_j = []
        correction_j = []
        for j in range(Nloops):
            print(samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
            y_j.append(t_cross)
            correction_j.append(-1*i*phase_time - t_cross)
        median_array.append(np.median(np.asarray(y_j)))
        correction_median_array.append(np.median(np.asarray(correction_j)))
    correction_median_array = np.asarray(correction_median_array)
    correction_median_array = correction_median_array + median_array[0]

    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/averages_splined/phase=33/phase_'+shaping+'/'
    Nloops = len(os.listdir(filedir))   #establishes length to cycle through file
    for i in range(Nloops):
        filename = filedir + 'Phase--waveforms--%05d.txt' % i
        (t,v,_) = rw(filename,numhead)
        t_avg,v_avg = boxcar_wf(t,v,n_box)
        v_delay = delay_wf(v_avg,n_delay)
        v_att = attenuate_wf(v_avg,n_att)
        v_sum = sum_wf(v_att,v_delay)
        t_cross,index_Cross,index_Peak = zc_locator(t_avg,v_sum)

        fig,ax = plt.subplots()
        ax.plot(t_avg,v_sum)   #plots CFD'd waveforms
        ax.plot(t_avg,v_delay,color = 'green')  #plots original/delayed waveform
        ax.plot(t_avg,v_att,color='purple')    #plots inverted/attenuated waveform
        #plots scatters of each index
        ax.scatter(t_avg,v_sum)
        ax.scatter(t_avg,v_delay,color = 'green')
        ax.scatter(t_avg,v_att,color='purple')
        ax.axhline(y=0,color='black')  #creates 0 axis
        ax.axvline(x=t_cross,color='red')  #creates line at zero crossing time
        ax.axvline(x=(-33*phase_time + median_array[0]),color='black')
        #plots index of peak and index used for crossing 0
        ax.plot(t_avg[index_Cross],v_sum[index_Cross],'x',color = 'orange')
        ax.plot(t_avg[index_Peak],v_sum[index_Peak],'x',color = 'yellow')
        #estabishes title and labels
        ax.set_title('D3--waveforms--%05d\nnbox= ' % i + str(n_box) + ' ndelay= ' + str(n_delay) + ' natt= ' + str(n_att) + '\nsubfolder = ' + shaping + '\nCrossing Time = %05gs' % t_cross)
        ax.set_xlabel('Time')
        ax.set_ylabel('Bits')
        #shows plot
        plt.get_current_fig_manager().window.showMaximized()
        plt.show(block = False)
        if ((-33*phase_time + median_array[0]) - t_cross) <= -3e-12:
            savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/disparity/averages_splined/bad/'
        else:
            savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/disparity/averages_splined/good/'
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        filename = 'Waveform_%d.png' % i
        savename = savedir + filename
        fig.savefig(savename,dpi = 500)
        plt.close()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="plot waveform",description="cycles through CFD waveforms and plots them.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw_gained_analyzed')
    parser.add_argument('--n_box',type=int,help='n value for boxcar averager',default = 2)
    parser.add_argument('--n_delay',type=int,help='number of indices to delay base waveform',default = 1)
    parser.add_argument('--n_att',type=int,help='amount to attenuate inverted waveform by, must be base 2',default = 2)
    parser.add_argument('--samplerate',type = str,help = 'downsampled rate to analyze (1 Gsps, 500 Msps, 250 Msps, 125 Msps)',default = '250 Msps')
    args = parser.parse_args()

    plot_waveform(args.datadate,args.numhead,args.subfolder,args.n_box,args.n_delay,args.n_att,args.samplerate)