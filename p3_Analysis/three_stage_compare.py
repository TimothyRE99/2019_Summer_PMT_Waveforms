#takes in the three stages of waveform and plots them, normalized, on each other

#import necessary
import numpy as np
from matplotlib import pyplot as plt
from readwaveform import read_waveform as rw

#plotting function
def three_stage_compare(datadate,numhead,filenum,shaping):
    readname1 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/D1--waveforms--%05d.txt' % filenum
    readname2 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d2/d2_' + shaping + '_gained/D2--waveforms--%05d.txt' % filenum
    readname3 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d3/d3_' + shaping + '_gained_analyzed/D3--waveforms--%05d.txt' % filenum
    (t1,v1,_) = rw(readname1,numhead)
    (t2,v2,_) = rw(readname2,numhead)
    (t3,v3,_) = rw(readname3,numhead)
    v1 = v1/min(v1)
    v2 = v2/min(v2)
    v3 = v3/min(v3)
    plt.plot(t1,v1,color='orange')
    plt.plot(t2,v2,color='green')
    plt.plot(t3,v3,color='blue')
    plt.scatter(t3,v3,color='blue')
    plt.xlabel('Time (s)')
    plt.title('Orange = d1\nGreen = d2\nBlue = d3')
    plt.show()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="three_stage_compare",description="Gathers and plots three versions of the same waveform.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--filenum",type=float,help="hz, samples/s",default=0)
    parser.add_argument("--shaping",type=str,help="hz, samples/s of new digitizer",default='raw')
    args = parser.parse_args()

    three_stage_compare(args.datadate,args.numhead,args.filenum,args.shaping)