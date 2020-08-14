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
    chi2 = np.sum(np.true_divide(np.square(observed - expected),expected))
    return(chi2)

def fitter_timing(datadate,numhead,samplerate,samplerate_name,shaping):
    if samplerate_name == 'INVALID':
        return("Failed")
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    t_fitter,v_fitter,_ = rw('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt',1)
    uspl = us(t_fitter,v_fitter)
    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/'
    Nloops = len(os.listdir(filedir + 'phase=0/phase_'+shaping))
    difference_list = []
    for i in range(Nloops):
        print(i)
        j = random.randint(0,maxphase - 1)
        filename = filedir + 'phase='+str(j)+'/phase_'+shaping+'/Phase--waveforms--%05d.txt' % i
        t,v,_ = rw(filename,5)
        v = -1*v
        v_max = np.amax(v)
        i2 = np.where(v == v_max)[0][0]
        i1 = i2 - 1
        i3 = i2 + 1
        if v[i1] == 0:
            i1 = i2 + 2
        ET = np.array([t[i1],t[i2],t[i3]])
        EV = np.array([v[i1],v[i2],v[i3]])
        chi2_min = -1
        x_min = -1
        shift_min = -1
        shifts = np.arange(0,80/20000000000,1/20000000000)
        for shift in shifts:
            pre_OV = uspl(ET + shift)
            pre_OV_square = np.square(pre_OV)
            pre_bott = np.true_divide(pre_OV_square,EV)
            top = np.sum(pre_OV)
            bott = np.sum(pre_bott)
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
        if (-1*j*phase_time - t_cross) < -1.2e-7:
            plt.plot(t,v)
            plt.plot(t_fitter,v_fit)
            plt.scatter(ET,EV)
            plt.get_current_fig_manager().window.showMaximized()
            plt.show()
        difference_list.append(-1*j*phase_time - t_cross)
    difference_list = np.asarray(difference_list)
    ##histo_mean,histo_std = gauss_histogram(difference_list)
    ##difference_list = difference_list[(difference_list >= histo_mean - 10*histo_std) & (difference_list <= histo_mean + 10*histo_std)]
    true_mean = '%5g' % np.mean(difference_list)
    true_std = '%5g' % np.std(difference_list)
    histo_data, bins_data = np.histogram(difference_list, bins = 200)
    binwidth = (bins_data[1] - bins_data[0])                    #determining bin width
    #determining bin centers
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    ##b_guess = (len(difference_list) * binwidth)   #using area approximation to guess at B value
    ##popt, _ = cf(fit_function,xdata = binscenters,ydata = histo_data, p0 = [b_guess,histo_mean,histo_std], maxfev = 10000)
    ##gauss_mean = '%s' % float('%.5g' % popt[1])
    ##gauss_std = '%s' % float('%.5g' % popt[2])
    #establishing 5 significant figure versions of the mean and std from curve fit
    ##x_values = np.linspace(popt[1] - 1.5*popt[2], popt[1] + 1.5*popt[2], 100000)    #creating 100,000 x values to map curvefit gaussian to
    plt.rcParams.update({'font.size': 14})
    plt.bar(binscenters, histo_data, width=binwidth)        #plotting histogram
    ##plt.plot(x_values, fit_function(x_values, *popt), color='darkorange')   #plotting curve fit
    plt.xlabel('True Timing - Recovered Timing')
    plt.ylabel('Count')
    plt.title('Corrected Timings\nGaussian Fit Values:\nMean = '+true_mean+' seconds\nStandard Deviation = '+true_std+' seconds')
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