#lowpass filter calculation for use in p2

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw

#low pass filter
def lpfFirstOrder(v,tau,fsps):
    alpha = 1-np.exp(-1/(fsps*tau))
    y = np.zeros(len(v))
    for i in range(len(v)):
        if i == 0:
            y[i] = v[i]
        else:
            y[i] = v[i]*alpha + (1-alpha)*y[i-1]
    return y

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2 lowpass",description="applies lowpass filter to waveform.")
    parser.add_argument("--numhead",type=int,help='number of header lines to skip in the raw file',default=5)
    parser.add_argument("--filename",type=str,help="filename",default='g:/data/watchman/20190516_watchman_spe/d2/d2_raw/D2--waveforms--00000.txt')
    parser.add_argument("--tau",type=str,help="tau value",default=0.00000001)
    parser.add_argument("--fsps",type=str,help="hz, samples/s",default=20000000000)
    args = parser.parse_args()

    t,v,header = rw(args.filename,args.numhead)
    y = lpfFirstOrder(v,args.tau,args.fsps)
    print(header)
    plt.plot(t,v,color = 'blue')
    plt.plot(t,y,color = 'red')
    plt.show()