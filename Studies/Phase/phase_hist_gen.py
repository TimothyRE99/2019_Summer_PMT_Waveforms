#import necessary
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from readwaveform import read_waveform as rw

#runs boxcar averaging algorithm
def boxcar_wf(t,v,n):
    if(n==0):       #returns standard values if n = 0
        return t,v
    #reduces length of array by n if n > 0
    v1 = np.zeros(len(v)-n)
    t1 = np.zeros(len(t)-n)
    #runs boxcar moving average on array
    for i in range(len(v1)): 
        vsum = 0
        for j in range(n):
            vsum += v[n+i-j]
        v1[i]=float(vsum)/float(n)
        t1[i] = t[i] 
    return t1,v1

#runs delay of waveform
def delay_wf(v,n):
    #pads beginning of array with n 0's and removes n final indices
    v_insert = np.zeros(n)
    v1 = np.insert(v,0,v_insert)[:-n]
    return v1

#runs inversion and attenuation of waveform
def attenuate_wf(v,n):
    v1 = -1 * v     #inverts waveform
    #doesn't attenuate if n = 1
    if n == 1:
        return v1
    #divides by n otherwise
    v1 = v1 / n
    return v1

#sums waveforms together
def sum_wf(v_att,v_delay):
    v_sum = np.add(v_att,v_delay)       #adds waveforms together
    return v_sum

def zc_locator(t,v):
    stop_ind = int(len(v)/3)
    v_norm = v/max(v[0:stop_ind])     #normalizes for easy checking
    #creates array of "True" and "False" entries for where condition is met
    checkPeak = v_norm == 1
    checkCross = v_norm <= 0
    #turns into array of indices each value held above
    indexPeak = np.asarray([k for k, x in enumerate(checkPeak) if x])
    indexCross = np.asarray([k for k, x in enumerate(checkCross) if x])
    index_Peak = indexPeak[0]       #creates peak index into int
    #establishes first crossed index after peak
    indexCross_removed = indexCross[np.where(indexCross > index_Peak)]
    index_Cross = indexCross_removed[0]
    #interpolates time of crossing
    t_bef = t[index_Cross - 1]
    t_aft = t[index_Cross]
    v_bef = v[index_Cross - 1]
    v_aft = v[index_Cross]
    slope = (v_aft - v_bef) / (t_aft - t_bef)
    t_pass = (-1 * v_bef) / slope
    t_cross = t_bef + t_pass
    return (t_cross,index_Cross,index_Peak)

def phase_hist_gen(samplerate,samplerate_name,shaping,datadate,n_box,n_delay,n_att,numhead):
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    phase_array = np.arange(0,maxphase)
    x = []
    y = []
    x_bins = []
    median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        y_j = []
        x_j = []
        for j in range(Nloops):
            print(samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
            y_j.append(t_cross)
            x_j.append(-1*i*phase_time)
        median_array.append(np.median(np.asarray(y_j)))
        y = y + y_j
        x = x + x_j
        x_bins.append(-1*(i-0.5)*phase_time)
    y = np.asarray(y)
    y = y - median_array[0]
    median_array = np.asarray(median_array)
    median_array = median_array - median_array[0]
    ybin = 1/(2*samplerate)
    y_bins = np.linspace(-2*ybin,0,num=maxphase,endpoint = True)
    x_bins = np.asarray(x_bins)
    x_bins = np.flip(x_bins)
    fig,ax = plt.subplots()
    h = ax.hist2d(x,y,bins = [x_bins,y_bins])
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,median_array,c = 'Green')
    ax.plot(np.flip(x_bins)-0.5*phase_time,np.flip(x_bins)-0.5*phase_time,c = 'Green',ls = '--')
    ax.set_title('Measured vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Measured Timing (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/Histograms/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()
    return()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="phase_hist_gen",description="Generates 2D Histograms of timing resolution vs. phase.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    #for n_box in range(5):
    #    if n_box == 3:
    #        pass
    #    else:
    #        for n_delay in range(1,17):
    #            if n_delay != 1 and n_delay != 2 and n_delay != 4 and n_delay != 8 and n_delay !=  16:
    #                pass
    #            else:
    #                for n_att in range(1,5):
    #                    if n_att == 3:
    #                        pass
    #                    else:
    #                        phase_hist_gen(250000000,'250 Msps','raw_gained_analyzed',args.datadate,n_box,n_delay,n_att,args.numhead)

    phase_hist_gen(250000000,'250 Msps','raw_gained_analyzed',args.datadate,2,1,2,args.numhead)