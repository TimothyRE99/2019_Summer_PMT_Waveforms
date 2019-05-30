#Sorting function for p1
#Requires import of readwaveform.py and writewaveform.py for proper functioning

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
from scipy import signal
import os

#Sort the data
def p1_sort(filenum,datadate,lowpass,numhead,numtaps,threshold,baseline):
    filename = 'g:/data/watchman/'+datadate+'_watchman_spe/C2--waveforms--%05d.txt' % filenum
    spe_wasname = 'g:/data/watchman/'+datadate+'_watchman_spe/d1/d1_raw/D1--waveforms--%05d.txt' % filenum
    spe_not_there = 'g:/data/watchman/'+datadate+'_watchman_spe/d1/not_spe/D1--waveforms--%05d.txt' % filenum
    spe_unsure = 'g:/data/watchman/'+datadate+'_watchman_spe/d1/unsure_if_spe/D1--waveforms--%05d.txt' % filenum
    if os.path.isfile(spe_wasname):
        pass
    elif os.path.isfile(spe_not_there):
        pass
    elif os.path.isfile(spe_unsure):
        pass
    else:
        (t,v,header) = rw(filename,numhead)

        y = signal.filtfilt(lowpass,1.0,v)
        y2 = y[numtaps:len(y)-1]
        t2 = t[numtaps:len(y)-1]

        y_flip = -1*y2
        height = -1*(baseline+threshold)
        peaks, _ = signal.find_peaks(y_flip, height, distance = 350)
        y_peaks = y2[peaks]
        t_peaks = t2[peaks]

        if len(peaks) != 0:                                         #Making sure there is a peak
            if len(peaks) == 1 and peaks[0] >= 450:                 #Checking if only 1 peak exists, making sure it's in proper range
                if min(y2[370:1370]) < baseline+threshold:                     #Checking if peak is below -.0015V in range 370 to 1370
                    write_waveform(t2, y2, spe_wasname, header)
                    print(len(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d1/d1_raw/')))
            else:
                if min(y2[370:1370]) < baseline+threshold:                 #Shows plot if min is less than -0.0015V in range 370 to 1370
                    plt.figure()
                    plt.plot(t,v,'b')
                    plt.plot(t2,y2,'r',linewidth=2.5)
                    plt.plot(t_peaks,y_peaks,'x',color='cyan')
                    plt.grid(True)
                    print('Displaying file #%05d' % filenum)
                    plt.show(block = False)
                    plt.pause(5)
                    plt.close()

                    spe_check = 'pre-loop initialization'
                    while spe_check != 'y' and spe_check != 'u' and spe_check != 'n':
                        spe_check = input('Is there a single visible SPE? "y" or "n" or "u"\n')
                    #writing data to proper folder
                    if spe_check == 'y':
                        write_waveform(t2,y2,spe_wasname,header)
                    elif spe_check == 'n':
                        write_waveform(t2,y2,spe_not_there,header)
                    elif spe_check == 'u':
                        write_waveform(t2,y2,spe_unsure,header)
                    print('File #%05d: Done' % filenum)
                    print(len(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d1/d1_raw/')))
    return

if __name__ == '__main__':
    lowpass_default = signal.firwin(50, cutoff = .5, window = 'blackman')    #blackman windowed lowpass filter
    import argparse
    parser = argparse.ArgumentParser(prog='p1 sort', description='Sorting through raw data to find good SPEs')
    parser.add_argument('--filenum',type = int,help = 'file number to begin at')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type = int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--numtaps',type = int,help='length of filter',default=51)
    parser.add_argument('--threshold',type = int,help='voltage threshold',default=-0.0015)
    parser.add_argument('--baseline',type = int,help='baseline voltage, must be <= 0',default=0)
    args = parser.parse_args()

    p1_sort(args.filenum, args.datadate, lowpass_default, args.numhead, args.numtaps, args.threshold, args.baseline)