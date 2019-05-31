#sorts out double SPEs based on peak and charge histograms

#import necessary
import numpy as np
from info_file import info_file
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import matplotlib.pyplot as plt

#sorting out double SPEs
def p1b_sort(datadate,charge_mean,peak_mean,FWHM_mean,numhead):
    #set file locations for charge and peak histograms
    charge_name = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/charge.txt'
    peak_name = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/peak_amplitude.txt'
    #initialize histogram arrays
    charge_histo = np.array([])
    peak_histo = np.array([])
    FWHM_histo = np.array([])
    #read histogram txt files int othe arrays
    charge_fin = open(charge_name,'r')
    for line in charge_fin:
        charge_histo = np.append(charge_histo, float(line.split(',')[0]))
    charge_fin.close
    peak_fin = open(peak_name,'r')
    for line in peak_fin:
        peak_histo = np.append(peak_histo, float(line.split(',')[0]))
    peak_fin.close
    FWHM_fin = open(peak_name,'r')
    for line in FWHM_fin:
        FWHM_histo = np.append(peak_histo, float(line.split(',')[0]))
    FWHM_fin.close
    #setting up arrays listing indices of where the value is twice the mean or greater
    charge_doubles = np.asarray(charge_histo >= 2*charge_mean).nonzero()
    charge_doubles = charge_doubles[0]
    peak_doubles = np.asarray(peak_histo >= 2*peak_mean).nonzero()
    peak_doubles = peak_doubles[0]
    FWHM_doubles = np.asarray(FWHM_histo >= 2*FWHM_mean).nonzero()
    FWHM_doubles = FWHM_doubles[0]
    for i in range(len(charge_histo)):
        print(i)
        #setting location of files to read
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
        #setting up locations to write each file to
        writename_double = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_doubles/D1--waveforms--%05d.txt' % i
        writename_single = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/D1--waveforms--%05d.txt' % i
        t,v,header = rw(filename,numhead)                                   #reading data from waveform file
        if (np.any(charge_doubles == i) and np.any(peak_doubles == i)) or (np.any(FWHM_doubles == i) and np.any(charge_doubles == i)):       #checking if both charge and peak are greater than twice the mean
            print("Was double!")
            write_waveform(t,v,writename_double,header)
        elif any([np.any(charge_doubles == i), np.any(peak_doubles == i), np.any(FWHM_doubles == i)]):
            if np.any(charge_doubles == i):
                print("Charge")
            if np.any(peak_doubles == i):
                print("Peak")
            if np.any(FWHM_doubles == i):
                print("FWHM")
            plt.plot(t,v)
            plt.show()
            double_check = 'Initialization.'
            while double_check != 's' and double_check != 'd':
                double_check = input('Is there a single or double? "s" or "d"\n')
            if double_check == 's':
                write_waveform(t,v,writename_single,header)
            if double_check == 'd':
                print("Was double!")
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
    parser.add_argument('--FWHM_mean',type = float,help = 'mean calculated from peak histogram plot', default = 7.9859e-9)
    parser.add_argument('--numhead',type = int,help = 'number of lines to skip for header', default = 5)
    args = parser.parse_args()

    p1b_sort(args.datadate,args.charge_mean,args.peak_mean,args.FWHM_mean,args.numhead)
    info_file(args.datadate)                    #generate d1_info.txt file