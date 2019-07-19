#takes in the three stages of waveform and plots them, normalized, on each other

#import necessary
import numpy as np
from matplotlib import pyplot as plt
from readwaveform import read_waveform as rw

#plotting function
def three_stage_compare(datadate,numhead,filenum,shaping):
    plt.rcParams.update({'font.size': 16})
    readname1 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/D1--waveforms--%05d.txt' % filenum
    readname2 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d2/d2_' + shaping + '_gained/D2--waveforms--%05d.txt' % filenum
    readname3 = 'G:/Data/watchman/'+datadate+'_watchman_spe/d3/d3_' + shaping + '_gained_analyzed/D3--waveforms--%05d.txt' % filenum
    (t1,v1,_) = rw(readname1,numhead)
    (t2,v2,_) = rw(readname2,numhead)
    (t3,v3,_) = rw(readname3,numhead)
    v1 = v1/min(v1)
    v2 = v2/min(v2)
    v3 = v3/min(v3)
    p1, = plt.plot(t1,v1,color='orange',label='Waveform After P1')
    p2, = plt.plot(t2,v2,color='green',label='Waveform After P2')
    p3, = plt.plot(t3,v3,color='blue',label='Waveform After P3')
    plt.scatter(t3,v3,color='blue')
    plt.xlabel('Time (s)')
    plt.title('250 Msps, Risetime Octupled During P2\nSample SPE Waveform After Each Stage:\nWaveform %05d' % filenum)
    plt.legend(handles=[p1,p2,p3])
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="three_stage_compare",description="Gathers and plots three versions of the same waveform.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--filenum",type=float,help="hz, samples/s",default=6)
    parser.add_argument("--shaping",type=str,help="hz, samples/s of new digitizer",default='rise_octupled')
    args = parser.parse_args()

    three_stage_compare(args.datadate,args.numhead,args.filenum,args.shaping)