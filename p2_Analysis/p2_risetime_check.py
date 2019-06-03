#checks tau vs. rise time for average waveform

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from p2_lowpass import lpfFirstOrder as lpf
import os
import matplotlib.pyplot as plt

#generating average waveform
def average_waveform(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw')) - 1
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/D2--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        y = y/min(y)                #normalizing y values
        #starting array if this is first file
        if i == 0:
            ysum = y
        #adding additional normalized files to the array index-wise
        else:
            ysum = np.add(ysum,y)
    yfinal = np.divide(ysum,Nloops)
    return (t,yfinal)

#checking tau vs. rise time
def risetime_check(datadate,numhead,x_values,fsps):
    (t,v) = average_waveform(datadate,numhead)
    tau_check = np.linspace(1e-9,5e-6,x_values)
    risetime = np.array([])
    for i in range(len(tau_check)):
        print(i)
        v_taued = lpf(v,tau_check[i],fsps)
        v_norm = v_taued/max(v_taued)
        check10 = v_norm <= .1                                      #determining where 10% and 90% are located
        check90 = v_norm >= .9
        index10 = np.asarray([k for k, x in enumerate(check10) if x])
        index90 = np.asarray([k for k, x in enumerate(check90) if x])
        index_90 = int(index90[0])
        index10_removed = index10[np.where(index10 < index_90)]     #removing all values after 90% rise index
        index_10 = int(index10_removed[len(index10_removed)-1])     #turning last 10% rise index into int
        rise_time = float(t[index_90] - t[index_10])                  #rise time is time at 90% - time at 10%
        risetime = np.append(risetime,rise_time)
    fig = plt.figure(figsize=(6,4))
    plt.plot(tau_check,risetime)
    plt.axhline(y=7.1686e-9,color='red')
    plt.axhline(y=1.43372e-8,color='orange')
    plt.axhline(y=2.86744e-8,color='yellow')
    idx_doub = int(np.argwhere(np.diff(np.sign(risetime - 7.1686e-9))).flatten()[0])
    idx_quart = int(np.argwhere(np.diff(np.sign(risetime - 1.43372e-8))).flatten()[0])
    idx_oct = int(np.argwhere(np.diff(np.sign(risetime - 2.86744e-8))).flatten()[0])
    plt.title('Double Risetime Tau = '+str(tau_check[idx_doub])+'\nQuadruple Risetime Tau = '+str(tau_check[idx_quart])+'\nOctuple Risetime Tau = '+str(tau_check[idx_oct]))
    plt.xlabel("Tau")
    plt.ylabel("10-90 Rise Time")
    plt.show()
    fig.savefig('G:/data/watchman/'+datadate+'_watchman_spe/d2/tau_compare.png',dpi = 500)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2 risetime check",description="Runs lowpass program on average waveforms to compare rise times")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--x_values",type=int,help="number of taus to generate",default=50000)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    args = parser.parse_args()

    risetime_check(args.datadate,args.numhead,args.x_values,args.fsps)