#Remove baseline from files to line up closer to 0

#import necessay
import numpy as np
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#shift baseline
def baselineshift(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_renamed'))    #establish size of directory
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted/'):    #create write directory if nonexistant
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted/')
    for i in range(Nloops):
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_renamed/D1--waveforms--%05d.txt' % i   #establish file name to read
        writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_baseline_shifted/D1--waveforms--%05d.txt' % i #establish file name to write
        (t,y,header) = rw(filename,numhead) #collect waveform data into array
        baseline = np.mean(y[0:200])                            #determining average value at beginning to establish baseline
        if abs(baseline) >= 0.0005: #used to check baselines that are too big
                print(str(baseline)+', '+str(i))
        y_new = (y - baseline)                                  #reducing y to factor out baseline
        write_waveform(t,y_new,writename,header)    #writing waveforms

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='baselineshift', description='Removing baseline from data')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    baselineshift(args.datadate,args.numhead)