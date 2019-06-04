#take in waveform and apply low pass filters for 2, 4, and 8 times 10-90 rise time

#import necessary
import numpy as np
import os
from p2_lowpass import lpfFirstOrder as lpf
from readwaveform import read_waveform as rw
from writewaveform import write_waveform

#applying lowpass filter and writing
def p2_review(datadate,numhead,fsps,x_values):
    #establish directories for reading and writing waveforms
    filedir = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/'
    writedir_two = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled/'
    writedir_four = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled/'
    writedir_eight = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled/'
    #establishing length of raw directory and subtracting one due to info file
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw')) - 1
    #cycling through all waveform files in directory
    for i in range(Nloops):
        print("File: %05d" % i)
        #establishing file names for reading and writing
        filename = filedir + 'D2--waveforms--%05d.txt' % i
        writename_two = writedir_two + 'D2--waveforms--%05d.txt' % i
        writename_four = writedir_four + 'D2--waveforms--%05d.txt' % i
        writename_eight = writedir_eight + 'D2--waveforms--%05d.txt' % i
        #checking which files exist, just doubles, doubles and quads, or all three
        if os.path.exists(writename_two) and os.path.exists(writename_four) and os.path.exists(writename_eight):        #all three
            print("All Exist!")
        elif os.path.exists(writename_two) and os.path.exists(writename_four):              #doubles and quads
            print("Octuples don't exist!")
            (t,v,header) = rw(filename,numhead)         #taking in information from waveform
            #removing baseline
            baseline = np.mean(v[0:100])
            v = (v - baseline)
            #establishing base risetime
            v_norm_notau = v/min(v)
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
            #determining tau vs. risetime
            tau_check = np.linspace(1e-5,1,x_values)                    #setting up tau values
            risetime = np.array([])                                     #initializing risetime array
            for i in range(len(tau_check)):                             #cycling through tau values
                if i % 100 == 0:
                    print(i)
                v_taued = lpf(v,tau_check[i],fsps)                      #applying tau value LPF
                v_norm = v_taued/min(v_taued)                           #normalizing result
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
            print(risetime[0])
            print(rise_time_notau*4)
            print(rise_time_notau*8)
            print(risetime[len(risetime)-1])
            #calculating intersection point of lines and tau vs. risetime
            if np.any(risetime > rise_time_notau*8) and np.any(risetime < rise_time_notau*8):
                idx_oct = int(np.argwhere(np.diff(np.sign(risetime - (rise_time_notau*8)))).flatten()[0])
                octuples = True
            else:
                print("No Octuples!")
                octuples = False
            #setting taus based on value necessary to double, quadruple, and octuple rise time
            if octuples:
                tau_eight = tau_check[idx_oct]
            #running low pass filter for each tau
            if octuples:
                y_eight = lpf(v,tau_eight,fsps)
            #writing results of each lpf to proper location
            if octuples:
                write_waveform(t,y_eight,writename_eight,header)
        elif os.path.exists(writename_two):                                 #just doubles
            print("Quadruples and Octuples don't exist!")
            (t,v,header) = rw(filename,numhead)         #taking in information from waveform
            #removing baseline
            baseline = np.mean(v[0:100])
            v = (v - baseline)
            #establishing base risetime
            v_norm_notau = v/min(v)
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
            #determining tau vs. risetime
            tau_check = np.linspace(1e-5,1,x_values)                    #setting up tau values
            risetime = np.array([])                                     #initializing risetime array
            for i in range(len(tau_check)):                             #cycling through tau values
                if i % 100 == 0:
                    print(i)
                v_taued = lpf(v,tau_check[i],fsps)                      #applying tau value LPF
                v_norm = v_taued/min(v_taued)                           #normalizing result
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
            print(risetime[0])
            print(rise_time_notau*4)
            print(rise_time_notau*8)
            print(risetime[len(risetime)-1])
            #calculating intersection point of lines and tau vs. risetime
            if np.any(risetime > rise_time_notau*8) and np.any(risetime < rise_time_notau*8):
                idx_oct = int(np.argwhere(np.diff(np.sign(risetime - (rise_time_notau*8)))).flatten()[0])
                octuples = True
            else:
                print("No Octuples!")
                octuples = False
            if np.any(risetime > rise_time_notau*4) and np.any(risetime < rise_time_notau*4):
                idx_quart = int(np.argwhere(np.diff(np.sign(risetime - (rise_time_notau*4)))).flatten()[0])
                quadruples = True
            else:
                print("No Quadruples!")
                quadruples = False
            #setting taus based on value necessary to double, quadruple, and octuple rise time
            if quadruples:
                tau_four = tau_check[idx_quart]
            if octuples:
                tau_eight = tau_check[idx_oct]
            #running low pass filter for each tau
            if quadruples:
                y_four = lpf(v,tau_four,fsps)
            if octuples:
                y_eight = lpf(v,tau_eight,fsps)
            #writing results of each lpf to proper location
            if quadruples:
                write_waveform(t,y_four,writename_four,header)
            if octuples:
                write_waveform(t,y_eight,writename_eight,header)
        else:
            print("None Exist!")

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="p2_review",description="Runs lowpass program on waveforms missed before to increase rise time by appropriate amount")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--fsps",type=float,help="hz, samples/s",default=20000000000.0)
    parser.add_argument("--x_values",type=int,help="number of taus to generate",default=5000)
    args = parser.parse_args()

    p2_review(args.datadate,args.numhead,args.fsps,args.x_values)