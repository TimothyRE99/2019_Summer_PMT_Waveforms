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

def fitter_timing(datadate,samplerate,samplerate_name,shaping):
    if samplerate_name == 'INVALID':
        return("Failed")
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    t_fitter,v_fitter,_ = rw('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt',1)
    uspl = us(t_fitter,v_fitter)
    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/'
    doubles_dir = 'G:/data/watchman/20190724_watchman_spe/studies/phase/Histograms/250 Msps/Doubles Combined/'
    doubles_array = os.listdir(doubles_dir)
    print(doubles_array)
    Nloops = len(os.listdir(filedir + 'phase=0/phase_'+shaping))
    difference_list = []
    chi_list = []
    for i in range(Nloops):
        print(i)
        if '%05d.png' % i in doubles_array:
            print('Skipped!')
        else:
            j = random.randint(0,maxphase - 1)
            filename = filedir + 'phase='+str(j)+'/phase_'+shaping+'/Phase--waveforms--%05d.txt' % i
            ##filename_exact = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/d3/d3_raw_gained/D3--waveforms--%05d.txt' % i
            t,v,_ = rw(filename,5)
            v = -1*v
            ##t_exact,v_exact,_ = rw(filename_exact,5)
            ##t_exact -= 1*j*phase_time
            ##time_locator = t[4]
            ##t_min_array = abs(t_exact - time_locator)
            ##time_index = np.where(t_min_array == np.amin(t_min_array))[0][0]
            ##v_exact = v_exact * v[4]/v_exact[time_index]
            ET = t[0:10]
            EV = v[0:10]
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
            ##if -1*j*phase_time - t_cross <= -1e-9 or chi2_min >= 2750 or -1*j*phase_time - t_cross >= 1e-9:
            ##    fig,ax = plt.subplots()
            ##    ax.plot(t,v)
            ##    ax.plot(t_fitter,v_fit)
            ##    ax.plot(t_exact,v_exact)
            ##    ax.scatter(ET,EV)
            ##    ax.axvline(-1*j*phase_time,color = 'Black')
            ##    ax.axvline(t_cross,color = 'Red')
            ##    ax.set_title(str(-1*j*phase_time - t_cross) + ', ' + str(chi2_min) + ', ' + str(i) + ', ' + str(j))
            ##    plt.get_current_fig_manager().window.showMaximized()
            ##    plt.show(block = False)
            ##    plt.pause(0.1)
            ##    fig.savefig('G:/data/watchman/20190724_watchman_spe/studies/phase/Histograms/250 Msps/Doubles/%05d.png' % i,dpi = 500)
            ##    print("Was double!")
            ##    plt.close()
            ##else:
            ##    difference_list.append((-1*j*phase_time - t_cross)[0])
            ##    chi_list.append(chi2_min)
            difference_list.append((-1*j*phase_time - t_cross)[0])
            chi_list.append(chi2_min)
    difference_list = np.asarray(difference_list)
    chi_list = np.asarray(chi_list)
    true_mean = '%5g' % (np.mean(difference_list)*1e12)
    true_std = '%5g' % (np.std(difference_list)*1e12)
    bins = np.linspace(-2.2e-9,2.2e-9,num = 100)
    histo_data, bins_data = np.histogram(difference_list, bins = bins)
    binwidth = (bins_data[1] - bins_data[0])
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    FontSize = 32
    plt.rcParams.update({'font.size': FontSize})
    _,ax = plt.subplots()
    ax.bar(binscenters, histo_data, width=binwidth)
    ax.set_xlabel('True Timing - Recovered Timing')
    ax.set_ylabel('Count')
    ax.set_title(samplerate_name+' - Fitter Timings, Doubles Removed')
    ax.text(0.05, 0.95, 'Distribution Parameters:\nMean: '+true_mean+' ps\nStandard Deviation: '+true_std+' ps', transform=ax.transAxes, fontsize=FontSize, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='White', alpha=0.5))
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
    plt.close()

    bins = np.linspace(0,30200,num = 100)
    histo_data, bins_data = np.histogram(chi_list, bins = bins)
    binwidth = (bins_data[1] - bins_data[0])
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    plt.rcParams.update({'font.size': FontSize})
    plt.bar(binscenters, histo_data, width=binwidth,log=True)
    plt.xlabel('Chi Squared')
    plt.ylabel('Count')
    plt.title(samplerate_name+' - Chi Squared Counts - Fitter Timings, Doubles Removed')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
    plt.close()

    _,ax = plt.subplots()
    h = ax.hist2d(difference_list,chi_list,bins=65,norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.set_title(samplerate_name+' - Chi Squared vs. Timing Corrections - Fitter Timings, Doubles Removed')
    ax.set_xlabel('Timing Corrections')
    ax.set_ylabel('Chi Squared')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
    plt.close()
    return("Passed")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="fitter timing",description="Uses average waveform to fit for timing")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
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
    
    status = fitter_timing(args.datadate,args.samplerate,samplerate_name,args.shaping)
    print(status)