#import necessary
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from readwaveform import read_waveform as rw
import math

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
def mult_wf(v,n):
    #doesn't attenuate if n = 1
    if n == 1:
        return v
    #divides by n otherwise
    v = v * n
    return v

#sums waveforms together
def sum_wf(v_mult,v_avg):
    v_sum = np.add(v_mult,-1*v_avg)       #adds waveforms together
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
    index_2 = 4#indexCross_removed[0]
    #interpolates time of crossing
    index_1 = index_2 - 1
    index_3 = index_2 + 1
    #if v[index_3] >= v[index_2]:
    #if (v[index_1] - v[index_2]) > (v[index_2] - v[index_3]):
    #    index_1 = index_1  -  1
    #    index_2 = index_2  -  1
    #    index_3 = index_3  -  1
    x1 = t[index_1]
    x2 = t[index_2]
    x3 = t[index_3]
    y1 = v[index_1]
    y2 = v[index_2]
    y3 = v[index_3]
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    a = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    b = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    c = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom
    if a != 0:
        d = b**2-4*a*c
        if d < 0:
            return(5000,5000,5000,5000)
        else:
            cross_1 = (-b + math.sqrt(d))/(2*a)
            cross_2 = (-b - math.sqrt(d))/(2*a)
    else:
        slope = (y1 - y3) / (x1 - x3)
        zero_pass = (-1 * y1) / slope
        cross_1 = x1 + zero_pass
        cross_2 = 1e1000
    if x1 < cross_1 < x3:
        t_cross = cross_1
    else:
        t_cross = cross_2
    return (t_cross,index_1,index_2,index_3)

def phase_hist_gen(samplerate,samplerate_name,shaping,datadate,n_box,n_delay,n_att,numhead):
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    phase_array = np.arange(0,maxphase)
    skipped_count = 0
    x = []
    y = []
    x_bins = []
    median_array = []
    correction = []
    correction_median_array = []
    for i in range(len(phase_array)):
        #print(i)
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/averages_splined/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        y_j = []
        x_j = []
        correction_j = []
        for j in range(Nloops):
            print('Uncorrected Files '+samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_mult = mult_wf(v_delay,n_att)
            v_sum = sum_wf(v_mult,v_avg)
            t_cross,_,_,_ = zc_locator(t_avg,v_sum)
            if t_cross == 5000:
                skipped_count += 1
            else:
                y_j.append(t_cross)
                x_j.append(-1*i*phase_time)
                correction_j.append(-1*i*phase_time - t_cross)
        median_array.append(np.median(np.asarray(y_j)))
        correction_median_array.append(np.median(np.asarray(correction_j)))
        y = y + y_j
        x = x + x_j
        correction = correction + correction_j
        x_bins.append(-1*(i-0.5)*phase_time)
    y = np.asarray(y)
    y = y - median_array[0]
    correction = np.asarray(correction)
    correction = correction + median_array[0]
    correction_median_array = np.asarray(correction_median_array)
    correction_median_array = correction_median_array + median_array[0]
    median_value = median_array[0]
    median_array = np.asarray(median_array)
    median_array = median_array - median_array[0]
    ybin = 1/(2*samplerate)
    y_bins = np.linspace(-2*ybin,0,num=maxphase,endpoint = True)
    y_bins_corrections = np.linspace(-ybin,ybin,num=maxphase,endpoint = True)
    x_bins = np.asarray(x_bins)
    x_bins = np.flip(x_bins)

    fig,ax = plt.subplots()
    h = ax.hist2d(x,y,bins = [x_bins,y_bins],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,median_array,c = 'Green')
    ax.plot(np.flip(x_bins)-0.5*phase_time,np.flip(x_bins)-0.5*phase_time,c = 'Green',ls = '--')
    ax.set_title('Measured vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Measured Timing (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/Histograms/averages/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_log.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    fig,ax = plt.subplots()
    h = ax.hist2d(x,correction,bins = [x_bins,y_bins_corrections],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,correction_median_array,c = 'Green')
    ax.set_title('Timing Corrections vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Timing Corrections (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/Histograms/averages/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_corrections_log.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    y_corrected = []
    corrected_median_array = []
    corrected_corrections = []
    corrected_correction_median_array = []
    for i in range(len(phase_array)):
        #print(i)
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/averages_splined/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        corrected_corrections_j = []
        y_corrected_j = []
        for j in range(Nloops):
            print('Corrected Files '+samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_mult = mult_wf(v_delay,n_att)
            v_sum = sum_wf(v_mult,v_avg)
            t_cross,_,_,_ = zc_locator(t_avg,v_sum)
            if t_cross == 5000:
                pass
            else:
                t_corrected = t_cross - median_value + correction_median_array[i]
                y_corrected_j.append(t_corrected)
                corrected_correction = -1*i*phase_time - t_corrected
                corrected_corrections_j.append(corrected_correction)
        corrected_median_array.append(np.median(np.asarray(y_corrected_j)))
        corrected_correction_median_array.append(np.median(np.asarray(corrected_corrections_j)))
        y_corrected = y_corrected + y_corrected_j
        corrected_corrections = corrected_corrections + corrected_corrections_j
    y_corrected = np.asarray(y_corrected)
    corrected_correction_median_array = np.asarray(corrected_correction_median_array)
    corrected_corrections = np.asarray(corrected_corrections)

    fig,ax = plt.subplots()
    h = ax.hist2d(x,y_corrected,bins = [x_bins,y_bins],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,corrected_median_array,c = 'Green')
    ax.plot(np.flip(x_bins)-0.5*phase_time,np.flip(x_bins)-0.5*phase_time,c = 'Green',ls = '--')
    ax.set_title('Measured vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Measured Timing (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/Histograms/averages/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = 'corrected '+samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_log.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    fig,ax = plt.subplots()
    h = ax.hist2d(x,corrected_corrections,bins = [x_bins,y_bins_corrections],norm = LogNorm())
    plt.colorbar(h[3],ax = ax)
    ax.plot(np.flip(x_bins)-0.5*phase_time,corrected_correction_median_array,c = 'Green')
    ax.set_title('Timing Corrections vs. True Timing')
    ax.set_xlabel('True Timing (Seconds)')
    ax.set_ylabel('Timing Corrections (Seconds)')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show(block = False)
    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/Histograms/averages/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = 'corrected '+samplerate_name+'_'+shaping+'_nbox='+str(n_box)+'_ndel='+str(n_delay)+'_natt='+str(n_att)+'_corrections_log.png'
    savename = savedir + filename
    fig.savefig(savename,dpi = 500)
    plt.close()

    return(skipped_count)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="phase_hist_gen",description="Generates 2D Histograms of timing resolution vs. phase.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    args = parser.parse_args()

    skipped_count = phase_hist_gen(250000000,'250 Msps','raw_gained_analyzed',args.datadate,2,1,2,args.numhead)
    print("%d Files Skippepd!" % skipped_count)