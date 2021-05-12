#import necessary
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from readwaveform import read_waveform as rw

def phase_hist_gen(samplerate_name,shaping,datadate):
    phase_time = 1/20000000000

    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/array_data/'
    if shaping == 'raw_gained_analyzed_noised':
        shape_name = '_noised'
    elif shaping == 'raw_gained_analyzed_peaked':    
        shape_name = '_peaked'
    x = np.loadtxt(filedir+'established_x'+shape_name+'.csv', delimiter=',')
    y = np.loadtxt(filedir+'established_y'+shape_name+'.csv', delimiter=',')
    x_bins = np.loadtxt(filedir+'established_x_bins'+shape_name+'.csv', delimiter=',')
    y_bins = np.loadtxt(filedir+'established_y_bins'+shape_name+'.csv', delimiter=',')
    median_array = np.loadtxt(filedir+'established_median_array'+shape_name+'.csv', delimiter=',')
    correction = np.loadtxt(filedir+'established_correction'+shape_name+'.csv', delimiter=',')
    y_bins_corrections = np.loadtxt(filedir+'established_y_bins_corrections'+shape_name+'.csv', delimiter=',')
    correction_median_array = np.loadtxt(filedir+'established_correction_median_array'+shape_name+'.csv', delimiter=',')
    y_corrected = np.loadtxt(filedir+'established_y_corrected'+shape_name+'.csv', delimiter=',')
    corrected_median_array = np.loadtxt(filedir+'established_corrected_median_array'+shape_name+'.csv', delimiter=',')
    corrected_corrections = np.loadtxt(filedir+'established_corrected_corrections'+shape_name+'.csv', delimiter=',')
    corrected_correction_median_array = np.loadtxt(filedir+'corrected_correction_median_array'+shape_name+'.csv', delimiter=',')

    _,ax = plt.subplots()
    h = ax.hist2d(x,y,bins = [x_bins,y_bins],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,median_array,c = 'Green')
    ax.plot(np.flip(x_bins)-0.5*phase_time,np.flip(x_bins)-0.5*phase_time,c = 'Green',ls = '--')
    ax.set_title('Measured vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Measured Timing (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
    _,ax = plt.subplots()
    h = ax.hist2d(x,correction,bins = [x_bins,y_bins_corrections],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,correction_median_array,c = 'Green')
    ax.set_title('Timing Corrections vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Timing Corrections (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()

    _,ax = plt.subplots()
    h = ax.hist2d(x,y_corrected,bins = [x_bins,y_bins],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,corrected_median_array,c = 'Green')
    ax.plot(np.flip(x_bins)-0.5*phase_time,np.flip(x_bins)-0.5*phase_time,c = 'Green',ls = '--')
    ax.set_title('Measured vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Measured Timing (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()

    _,ax = plt.subplots()
    h = ax.hist2d(x,corrected_corrections,bins = [x_bins,y_bins_corrections],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,corrected_correction_median_array,c = 'Green')
    ax.set_title('Timing Corrections vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Timing Corrections (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()

    return()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="phase_hist_gen",description="Generates 2D Histograms of timing resolution vs. phase.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    args = parser.parse_args()

    phase_hist_gen(250000000,'250 Msps','raw_gained_analyzed_noised',args.datadate,2,1,2,args.numhead)