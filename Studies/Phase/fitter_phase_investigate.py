import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os
import random
import math
from readwaveform import read_waveform as rw
from writewaveform import write_waveform as ww
import scipy.interpolate as it
from scipy.optimize import curve_fit as cf
from unispline import unispline as us

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

def timing_extraction(t_fitter,v_fitter):
    v_fitter_max = np.amax(v_fitter)
    v_fitter_max_index = np.where(v_fitter == v_fitter_max)[0][0]
    v_fitter = v_fitter[0:v_fitter_max_index]
    v_fitter_zero = v_fitter_max/2
    v_fitter_zero_array = np.abs(v_fitter - v_fitter_zero)
    v_fitter_zero_index = np.where(v_fitter_zero_array == np.amin(v_fitter_zero_array))[0]
    t_cross = t_fitter[v_fitter_zero_index]
    return(t_cross)

def chi_squared(observed,expected):
    chi2 = np.sum(np.true_divide(np.square(observed - expected),expected+100))
    return(chi2)

def fitter_timing(datadate,numhead,samplerate,samplerate_name,shaping):
    if samplerate_name == 'INVALID':
        return("Failed")
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    phase_array = np.arange(0,maxphase)
    t_fitter,v_fitter,_ = rw('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt',1)
    uspl = us(t_fitter,v_fitter)
    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/'
    Nloops = len(os.listdir(filedir + 'phase=0/phase_'+shaping))
    x = []
    y = []
    x_bins = []
    median_array = []
    correction = []
    correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        y_j = []
        x_j = []
        correction_j = []
        for j in range(Nloops):
            print('Uncorrected Files '+samplerate_name+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            t,v,_ = rw(filename,5)
            v = -1*v
            v_max = np.amax(v)
            i2 = np.where(v == v_max)[0][0]
            i1 = i2 - 1
            i3 = i2 + 1
            ET = np.array([t[i1],t[i2],t[i3]])
            EV = np.array([v[i1],v[i2],v[i3]])
            chi2_min = -1
            x_min = -1
            shift_min = -1
            shifts = np.arange(0,80/20000000000,1/20000000000)
            for shift in shifts:
                pre_OV = uspl(ET + shift)
                top = np.sum(np.true_divide(np.multiply(pre_OV,EV),EV+100))
                bott = np.sum(np.true_divide(np.square(pre_OV),EV+100))
                x = top/bott
                OV = x*pre_OV
                chi2 = chi_squared(OV,EV)
                if chi2_min < 0:
                    shift_min = shift
                    chi2_min = chi2
                    x_min = x
                elif chi2 < chi2_min:
                    shift_min = shift
                    chi2_min = chi2
                    x_min = x
            v_fit = x_min*uspl(t_fitter + shift_min)
            t_cross = timing_extraction(t_fitter,v_fit)
            if (-1*i*phase_time - t_cross) < -1.e-7:
                plt.plot(t,v)
                plt.plot(t_fitter,v_fit)
                plt.scatter(ET,EV)
                plt.axvline(-1*i*phase_time,color = 'Black')
                plt.axvline(t_cross,color = 'Red')
                plt.get_current_fig_manager().window.showMaximized()
                plt.show()
            correction_j.append(-1*i*phase_time - t_cross)
        median_array.append(np.median(np.asarray(y_j)))
        correction_median_array.append(np.median(np.asarray(correction_j)))
        y = y + y_j
        x = x + x_j
        correction = correction + correction_j
        x_bins.append(-1*(i-0.5)*phase_time)
    y = np.asarray(y)
    y = y - median_array[0]
    correction = np.asarray(correction)
    correction = correction + median_array[0]
    correction_median_array = np.asarray(correction_median_array)
    correction_median_array = correction_median_array + median_array[0]
    median_value = median_array[0]
    median_array = np.asarray(median_array)
    median_array = median_array - median_array[0]
    ybin = 1/(2*samplerate)
    y_bins = np.linspace(-2*ybin,0,num=maxphase,endpoint = True)
    y_bins_corrections = np.linspace(-ybin,ybin,num=maxphase,endpoint = True)
    x_bins = np.asarray(x_bins)
    x_bins = np.flip(x_bins)

    fig,ax = plt.subplots()
    h = ax.hist2d(x,y,bins = [x_bins,y_bins],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,median_array,c = 'Green')
    ax.plot(np.flip(x_bins)-0.5*phase_time,np.flip(x_bins)-0.5*phase_time,c = 'Green',ls = '--')
    ax.set_title('Measured vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Measured Timing (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/Histograms/' + samplerate_name + '/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = 'fitter_recovered_uncorrected.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    fig,ax = plt.subplots()
    h = ax.hist2d(x,correction,bins = [x_bins,y_bins_corrections],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,correction_median_array,c = 'Green')
    ax.set_title('Timing Corrections vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Timing Corrections (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/Histograms/' + samplerate_name + '/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = 'fitter_corrections_uncorrected.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    y_corrected = []
    corrected_median_array = []
    corrected_corrections = []
    corrected_correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        corrected_corrections_j = []
        y_corrected_j = []
        for j in range(Nloops):
            print('Corrected Files '+samplerate_name+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            v = -1*v
            v_max = np.amax(v)
            i2 = np.where(v == v_max)[0][0]
            i1 = i2 - 1
            i3 = i2 + 1
            ET = np.array([t[i1],t[i2],t[i3]])
            EV = np.array([v[i1],v[i2],v[i3]])
            chi2_min = -1
            x_min = -1
            shift_min = -1
            shifts = np.arange(0,80/20000000000,1/20000000000)
            for shift in shifts:
                pre_OV = uspl(ET + shift)
                top = np.sum(np.true_divide(np.multiply(pre_OV,EV),EV+10))
                bott = np.sum(np.true_divide(np.square(pre_OV),EV+10))
                x = top/bott
                OV = x*pre_OV
                chi2 = chi_squared(OV,EV)
                if chi2_min < 0:
                    shift_min = shift
                    chi2_min = chi2
                    x_min = x
                elif chi2 < chi2_min:
                    shift_min = shift
                    chi2_min = chi2
                    x_min = x
            v_fit = x_min*uspl(t_fitter + shift_min)
            t_cross = timing_extraction(t_fitter,v_fit)
            t_corrected = t_cross - median_value + correction_median_array[i]
            y_corrected_j.append(t_corrected)
            corrected_correction = -1*i*phase_time - t_corrected
            corrected_corrections_j.append(corrected_correction)
        corrected_median_array.append(np.median(np.asarray(y_corrected_j)))
        corrected_correction_median_array.append(np.median(np.asarray(corrected_corrections_j)))
        y_corrected = y_corrected + y_corrected_j
        corrected_corrections = corrected_corrections + corrected_corrections_j
    y_corrected = np.asarray(y_corrected)
    corrected_correction_median_array = np.asarray(corrected_correction_median_array)
    corrected_corrections = np.asarray(corrected_corrections)

    fig,ax = plt.subplots()
    h = ax.hist2d(x,y_corrected,bins = [x_bins,y_bins],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,corrected_median_array,c = 'Green')
    ax.plot(np.flip(x_bins)-0.5*phase_time,np.flip(x_bins)-0.5*phase_time,c = 'Green',ls = '--')
    ax.set_title('Measured vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Measured Timing (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/Histograms/' + samplerate_name + '/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = 'fitter_recovered_corrected.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    fig,ax = plt.subplots()
    h = ax.hist2d(x,corrected_corrections,bins = [x_bins,y_bins_corrections],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,corrected_correction_median_array,c = 'Green')
    ax.set_title('Timing Corrections vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Timing Corrections (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/Histograms/' + samplerate_name + '/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = 'fitter_corrections_corrected.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

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