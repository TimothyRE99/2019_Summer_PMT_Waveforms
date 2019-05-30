#sorts out double SPEs based on peak and charge histograms

#import necessary
import numpy as np
import os
from info_file import info_file
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#sorting out double SPEs
def p1b_sort(datadate,charge_mean,peak_mean,numhead):
    charge_name = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/charge.txt'
    peak_name = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/peak_amplitude.txt'
    charge_histo = np.array([])
    peak_histo = np.array([])
    charge_fin = open(charge_name,'r')
    for line in charge_fin:
        charge_histo = np.append(charge_histo, float(line.split(',')[0]))
    charge_fin.close
    peak_fin = open(peak_name,'r')
    for line in peak_fin:
        peak_histo = np.append(peak_histo, float(line.split(',')[0]))
    peak_fin.close
    charge_doubles = np.where(charge_histo >= 2*charge_mean)
    peak_doubles = np.where(peak_histo >= 2*peak_mean)
    for i in range(len(charge_histo)):
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
        writename_double = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_doubles/D1--waveforms--%05d.txt' % i
        writename_single = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/D1--waveforms--%05d.txt' % i
        t,v,header = rw(filename,numhead)
        if i in charge_doubles and i in peak_doubles:
            write_waveform(t,v,writename_double,header)
        else:
            write_waveform(t,v,writename_single,header)
    return

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='p1b', description='Calculating doubles and running info_file.py')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--charge_mean',type = float,help = 'mean calculated from charge histogram plot', default = 1.6799e-12)
    parser.add_argument('--peak_mean',type = float,help = 'mean calculated from peak histogram plot', default = 0.0064251)
    parser.add_argument('--numhead',type = int,help = 'number of lines to skip for header', default = 5)
    args = parser.parse_args()

    p1b_sort(args.datadate,args.charge_mean,args.peak_mean,args.numhead)
    info_file(args.datadate)