#generates 2D histogram of timing resolution vs phase

#import necessary
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from readwaveform import read_waveform as rw

def phase_hist_gen(samplerate_name,shaping,datadate,n_box,n_delay,n_att):
    phase_time = 1/20000000000

    filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/array_data/'
    x = np.loadtxt(filedir+'x.csv', delimiter=',')
    y = np.loadtxt(filedir+'y.csv', delimiter=',')
    x_bins = np.loadtxt(filedir+'x_bins.csv', delimiter=',')
    y_bins = np.loadtxt(filedir+'y_bins.csv', delimiter=',')
    median_array = np.loadtxt(filedir+'median_array.csv', delimiter=',')
    correction = np.loadtxt(filedir+'correction.csv', delimiter=',')
    y_bins_corrections = np.loadtxt(filedir+'y_bins_corrections.csv', delimiter=',')
    correction_median_array = np.loadtxt(filedir+'correction_median_array.csv', delimiter=',')
    y_corrected = np.loadtxt(filedir+'y_corrected.csv', delimiter=',')
    corrected_median_array = np.loadtxt(filedir+'corrected_median_array.csv', delimiter=',')
    corrected_corrections = np.loadtxt(filedir+'corrected_corrections.csv', delimiter=',')
    corrected_correction_median_array = np.loadtxt(filedir+'corrected_correction_median_array.csv', delimiter=',')

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
    filename = samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_log.png'
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
    filename = samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_corrections_log.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

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
    filename = 'corrected '+samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_log.png'
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
    filename = 'corrected '+samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_corrections_log.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    return()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="phase_hist_gen",description="Generates 2D Histograms of timing resolution vs. phase.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    args = parser.parse_args()

    phase_hist_gen('250 Msps','raw_gained_analyzed',args.datadate,2,1,2)