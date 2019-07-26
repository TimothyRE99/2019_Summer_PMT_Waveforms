#determine peak amplitude of waveform

#import necessary
import numpy as np
import os
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh

def determine(datadate,numhead,directory,samplerate):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/' + samplerate + '/d3_'+directory+'_analyzed'))
    writename = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/' + samplerate + '/trigger_histograms/peak_amplitude_'+directory+'.txt'
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/' + samplerate + '/trigger_histograms/histogram_images'):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/' + samplerate + '/trigger_histograms/histogram_images')
    #peak amplitude acquisition
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/' + samplerate + '/d3_'+directory+'_analyzed/D3--waveforms--%05d.txt' % i
        (_,y,_) = rw(filename,numhead)
        index_min = np.where(y == min(y))               #determining index of peak
        value = str((-1*y[index_min])[0])               #flipping peak to positive
        wh(value,writename)                             #writing value to histogram txt file
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Bits","Histogram of Peak Amplitudes","Peak_Amplitude"+directory,datadate,histo_mean,histo_std,samplerate)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determinepeakamplitude', description='determining and writing histogram for peak amplitudes')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--directory',type=str,help='name of directory files read from',default = 'raw_gained')
    parser.add_argument('--samplerate',type = str,help = 'downsampled rate to analyze (1 Gsps, 500 Msps, 250 Msps, 125 Msps)',default = '1 Gsps')
    args = parser.parse_args()

    determine(args.datadate,args.numhead,args.directory,args.samplerate)