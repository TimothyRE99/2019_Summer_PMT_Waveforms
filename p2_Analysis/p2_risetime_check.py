#checks tau vs. rise time for average waveform

#import necessary
import numpy as np
from readwaveform import read_waveform as rw
from p2_lowpass import lpfFirstOrder as lpf
import os
import matplotlib.pyplot as plt
from writewaveform import write_waveform

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
    write_waveform(t,v,'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_average.txt',"Average Waveform")
    #determining rise time of average waveform
    v_norm_notau = v/max(v)
    #determining where 10% and 90% are located
    check10_notau = v_norm_notau <= .1
    check90_notau = v_norm_notau >= .9
    #converting to array of indices
    index10_notau = np.asarray([k for k, x in enumerate(check10_notau) if x])
    index90_notau = np.asarray([k for k, x in enumerate(check90_notau) if x])
    index_90_notau = int(index90_notau[0])
    index10_removed_notau = index10_notau[np.where(index10_notau < index_90_notau)]         #removing all values after 90% rise index
    index_10_notau = int(index10_removed_notau[len(index10_removed_notau)-1])               #turning last 10% rise index into int
    rise_time_notau = float(t[index_90_notau] - t[index_10_notau])                          #rise time is time at 90% - time at 10%
    print(rise_time_notau)
    #determining tau vs. risetime graph
    tau_check = np.linspace(1e-10,1e-5,x_values)                 #setting up tau values
    risetime = np.array([])                                     #initializing risetime array
    for i in range(len(tau_check)):                             #cycling through tau values
        print(i)
        v_taued = lpf(v,tau_check[i],fsps)                      #applying tau value LPF
        v_norm = v_taued/max(v_taued)                           #normalizing result
        #determining where 10% and 90% are located
        check10 = v_norm <= .1
        check90 = v_norm >= .9
        #converting to array of indices
        index10 = np.asarray([k for k, x in enumerate(check10) if x])
        index90 = np.asarray([k for k, x in enumerate(check90) if x])
        index_90 = int(index90[0])
        index10_removed = index10[np.where(index10 < index_90)]     #removing all values after 90% rise index
        index_10 = int(index10_removed[len(index10_removed)-1])     #turning last 10% rise index into int
        rise_time = float(t[index_90] - t[index_10])                #rise time is time at 90% - time at 10%
        risetime = np.append(risetime,rise_time)                    #appending risetime to risetime array
    fig = plt.figure(figsize=(6,4))                         #initializing figure saving
    plt.plot(tau_check,risetime)                            #plotting tau vs. risetime
    #plotting horizontal lines at 2x, 4x, and 8x risetime
    plt.axhline(y=(rise_time_notau*2),color='red')
    plt.axhline(y=(rise_time_notau*4),color='orange')
    plt.axhline(y=(rise_time_notau*8),color='yellow')
    #calculating intersection point of lines and tau vs. risetime
    idx_doub = int(np.argwhere(np.diff(np.sign(risetime - (rise_time_notau*2)))).flatten()[0])
    idx_quart = int(np.argwhere(np.diff(np.sign(risetime - (rise_time_notau*4)))).flatten()[0])
    idx_oct = int(np.argwhere(np.diff(np.sign(risetime - (rise_time_notau*8)))).flatten()[0])
    #setting up title (taus for each risetime value) and labels
    plt.title('Double Risetime Tau = '+str(tau_check[idx_doub])+'\nQuadruple Risetime Tau = '+str(tau_check[idx_quart])+'\nOctuple Risetime Tau = '+str(tau_check[idx_oct]))
    plt.xlabel("Tau")
    plt.ylabel("10-90 Rise Time")
    #showing and saving plot
    plt.show()
    fig.savefig('G:/data/watchman/'+datadate+'_watchman_spe/d2/tau_compare.png',dpi = 500)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2 risetime check",description="Runs lowpass program on average waveforms to compare rise times")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--x_values",type=int,help="number of taus to generate",default=100000)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    args = parser.parse_args()

    risetime_check(args.datadate,args.numhead,args.x_values,args.fsps)