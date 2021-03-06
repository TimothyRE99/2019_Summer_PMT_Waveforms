#Generates 1D Histograms of timing resolution with random sampled phase, no doubles included

#import necessary
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from readwaveform import read_waveform as rw
import random
from scipy.optimize import curve_fit as cf

def gauss_histogram(histo):
    histo = np.sort(histo)
    #splitting off array into upper and lower halves
    histo_low = np.array_split(histo,2)[0]
    histo_high = np.array_split(histo,2)[1]
    #determining median of each half (aka, 1st and 3rd quartiles)
    medi_low = np.median(histo_low)
    medi_high = np.median(histo_high)
    iqr = (medi_high - medi_low)                    #calculating inter-quartile range
    #calculating outlier thresholds
    out_low = (medi_low - 1.5*iqr)
    out_high = (medi_low + 1.5*iqr)
    histo_out_remove = histo[np.where((out_low <= histo) & (histo <= out_high))]    #creating new array with outliers removed
    #determining mean and std guesses for central data
    histo_mean = np.mean(histo_out_remove)
    histo_std = np.std(histo_out_remove)
    return (histo_mean,histo_std)

def fit_function(x,B,mu,sigma):
    #funcion for a gaussian scaled by factor B
    return (B * (1/np.sqrt(2 * np.pi * sigma**2)) * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))

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

def phase_hist_gen(samplerate,samplerate_name,shaping,datadate,n_box,n_delay,n_att,numhead):
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    doubles_dir = 'G:/data/watchman/20190724_watchman_spe/studies/phase/Histograms/250 Msps/Doubles Combined/'
    doubles_array = os.listdir(doubles_dir)
    
    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase=0/phase_'+shaping+'/'
    Nloops = len(os.listdir(filedir))

    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/array_data/'
    median_array = np.loadtxt(filedir+'median_array.csv', delimiter=',')
    correction_median_array = np.loadtxt(filedir+'correction_median_array.csv', delimiter=',')

    difference_list = []
    corrected_difference_list = []
    for j in range(Nloops):
        if '%05d.png' % j in doubles_array:
            print('Skipped!')
        else:
            print(j)
            i = random.randint(0,maxphase - 1)
            filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase='+str(i)+'/phase_'+shaping+'/'
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
            t_cross = t_cross - median_array[0]
            difference_list.append(-1*i*phase_time - t_cross)
            corrected_difference_list.append(-1*i*phase_time - (t_cross + correction_median_array[i]))

    difference_list = np.asarray(difference_list)
    corrected_difference_list = np.asarray(corrected_difference_list)

    #histo_mean,histo_std = gauss_histogram(corrected_difference_list)
    #corrected_difference_list = corrected_difference_list[(corrected_difference_list >= histo_mean - 10*histo_std) & (corrected_difference_list <= histo_mean + 10*histo_std)]
    true_mean = '%5g' % (np.mean(corrected_difference_list)*1e12)
    true_std = '%5g' % (np.std(corrected_difference_list)*1e12)
    bins = np.linspace(-2.2e-9,2.2e-9,num = 100)
    histo_data, bins_data = np.histogram(corrected_difference_list, bins = bins)
    binwidth = (bins_data[1] - bins_data[0])
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    #b_guess = (len(corrected_difference_list) * binwidth)
    #popt, _ = cf(fit_function,xdata = binscenters,ydata = histo_data, p0 = [b_guess,histo_mean,histo_std], maxfev = 10000)
    #x_values = np.linspace(popt[1] - 1.5*popt[2], popt[1] + 1.5*popt[2], 100000)
    FontSize = 32
    plt.rcParams.update({'font.size': FontSize})
    _,ax = plt.subplots()
    ax.bar(binscenters, histo_data, width=binwidth)
    #ax.plot(x_values, fit_function(x_values, *popt), color='darkorange')
    ax.set_xlabel('True Timing - Recovered Timing')
    ax.set_ylabel('Count')
    ax.set_title(samplerate_name+' - CFD Timings, Doubles Removed')
    ax.text(0.025, 0.95, 'Distribution Parameters:\nMean: '+true_mean+' ps\nStandard Deviation: '+true_std+' ps', transform=ax.transAxes, fontsize=FontSize, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='White', alpha=0.5))
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="timing_resolution_compare",description="Generates 1D Histograms of timing resolution with random sampled phase.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    phase_hist_gen(250000000,'250 Msps','raw_gained_analyzed',args.datadate,2,1,2,args.numhead)