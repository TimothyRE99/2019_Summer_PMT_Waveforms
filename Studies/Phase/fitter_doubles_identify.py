#identifies doubles and saves them to a doubles folder

#import necessary
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
    chi2 = np.sum(np.square(observed - expected))
    return(chi2)

def fitter_timing(datadate,samplerate_name,shaping):
    if samplerate_name == 'INVALID':
        return("Failed")
    t_fitter,v_fitter,_ = rw('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt',1)
    uspl = us(t_fitter,v_fitter)
    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/'
    Nloops = len(os.listdir(filedir + 'phase=0/phase_'+shaping))
    for i in range(Nloops):
        print(i)
        filename_exact = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/d3/d3_raw_gained/D3--waveforms--%05d.txt' % i
        t,v,_ = rw(filename_exact,5)
        v = -1*v
        ET = t[0:400]
        EV = v[0:400]
        chi2_min = -1
        x_min = -1
        y_min = -1
        shift_min = -1
        shifts = np.arange(0,80/20000000000,1e-11)
        for shift in shifts:
            pre_OV = uspl(ET + shift)
            A = np.array([[np.sum(np.square(pre_OV)),np.sum(pre_OV),np.sum(np.multiply(pre_OV,EV))],[np.sum(pre_OV),len(EV),np.sum(EV)]])
            A[0] = A[0]/A[0][0]
            A[1] = np.subtract(A[1],A[1][0]*A[0])
            A[1] = A[1]/A[1][1]
            A[0] = np.subtract(A[0],A[0][1]*A[1])
            x = A[0][2]
            y = A[1][2]
            OV = x*pre_OV + y
            chi2 = chi_squared(OV,EV)
            if chi2_min < 0:
                shift_min = shift
                chi2_min = chi2
                x_min = x
                y_min = y
            elif chi2 < chi2_min:
                shift_min = shift
                chi2_min = chi2
                x_min = x
                y_min = y
        v_fit = x_min*uspl(t_fitter + shift_min) + y_min
        t_cross = timing_extraction(t_fitter,v_fit)
        if t_cross <= -0.5e-10 or chi2_min >= 7.95e-5 or t_cross >= 0.5e-10:
            fig,ax = plt.subplots()
            ax.plot(t,v)
            ax.plot(t_fitter,v_fit)
            ax.axvline(0,color = 'Black')
            ax.axvline(t_cross,color = 'Red')
            ax.set_title(str(t_cross) + ', ' + str(chi2_min) + ', ' + str(i))
            plt.get_current_fig_manager().window.showMaximized()
            plt.show(block = False)
            plt.pause(0.1)
            fig.savefig('G:/data/watchman/20190724_watchman_spe/studies/phase/Histograms/'+samplerate_name+'/Doubles/%05d.png' % i,dpi = 500)
            print("Was double!")
            plt.close()
    return("Passed")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="fitter timing",description="Uses average waveform to fit for timing")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
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
    
    status = fitter_timing(args.datadate,samplerate_name,args.shaping)
    print(status)