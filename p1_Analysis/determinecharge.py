#Determining charge of waveforms

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from readhistogram import read_histogram as rh
from gausshistogram import gauss_histogram as gh
import os

def determine(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered'))
    writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/charge.txt'
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/histogram_images'):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/histogram_images')
    #determining charge
    for i in range(Nloops):
        print(i)
        area = 0
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_50centered/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        #determining area under curve
        for i in range(len(y)-1):
            area += ((t[i+1]-t[i]) * y[i])
        charge = str(-1*area/50)            #area under curve/resistance gives charge, made positive for graphical reasons
        wh(charge,writename)
    #create histogram from saved file
    (histo_mean,histo_std) = gh(writename)
    rh(writename,"Coulombs","Histogram of Charges","Charge",datadate,histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determinecharge', description='determining and writing histogram for charges')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    determine(args.datadate,args.numhead)