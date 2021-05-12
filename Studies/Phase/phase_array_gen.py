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

def phase_array_gen(samplerate,samplerate_name,shaping,datadate,n_box,n_delay,n_att,numhead):
    phase_time = 1/20000000000
    maxphase = int(20000000000/samplerate + 0.5)
    phase_array = np.arange(0,maxphase)

    x = []
    y = []
    x_bins = []
    median_array = []
    correction = []
    correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
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
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
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

    y_corrected = []
    corrected_median_array = []
    corrected_corrections = []
    corrected_correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/phase='+str(phase_array[i])+'/phase_'+shaping+'/'
        Nloops = len(os.listdir(filedir))
        corrected_corrections_j = []
        y_corrected_j = []
        for j in range(Nloops):
            print('Corrected Files '+samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
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

    established_x = []
    established_y = []
    established_x_bins = []
    established_median_array = []
    established_correction = []
    established_correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/file_template/phase='+str(phase_array[i])+'/phase_'+shaping+'_noised/'
        Nloops = len(os.listdir(filedir))
        established_y_j = []
        established_x_j = []
        established_correction_j = []
        for j in range(Nloops):
            print('Established Uncorrected Files '+samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
            established_y_j.append(t_cross)
            established_x_j.append(-1*i*phase_time)
            established_correction_j.append(-1*i*phase_time - t_cross)
        established_median_array.append(np.median(np.asarray(established_y_j)))
        established_correction_median_array.append(np.median(np.asarray(established_correction_j)))
        established_y = established_y + established_y_j
        established_x = established_x + established_x_j
        established_correction = established_correction + established_correction_j
        established_x_bins.append(-1*(i-0.5)*phase_time)
    established_y = np.asarray(established_y)
    established_y = established_y - established_median_array[0]
    established_correction = np.asarray(established_correction)
    established_correction = established_correction + established_median_array[0]
    established_correction_median_array = np.asarray(established_correction_median_array)
    established_correction_median_array = established_correction_median_array + established_median_array[0]
    established_median_value = established_median_array[0]
    established_median_array = np.asarray(established_median_array)
    established_median_array = established_median_array - established_median_array[0]
    established_ybin = 1/(2*samplerate)
    established_y_bins = np.linspace(-2*established_ybin,0,num=maxphase,endpoint = True)
    established_y_bins_corrections = np.linspace(-established_ybin,established_ybin,num=maxphase,endpoint = True)
    established_x_bins = np.asarray(established_x_bins)
    established_x_bins = np.flip(established_x_bins)

    established_y_corrected = []
    established_corrected_median_array = []
    established_corrected_corrections = []
    established_corrected_correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/file_template/phase='+str(phase_array[i])+'/phase_'+shaping+'_noised/'
        Nloops = len(os.listdir(filedir))
        established_corrected_corrections_j = []
        established_y_corrected_j = []
        for j in range(Nloops):
            print('Established Corrected Files '+samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
            established_t_corrected = t_cross - established_median_value + established_correction_median_array[i]
            established_y_corrected_j.append(established_t_corrected)
            established_corrected_correction = -1*i*phase_time - established_t_corrected
            established_corrected_corrections_j.append(established_corrected_correction)
        established_corrected_median_array.append(np.median(np.asarray(established_y_corrected_j)))
        established_corrected_correction_median_array.append(np.median(np.asarray(established_corrected_corrections_j)))
        established_y_corrected = established_y_corrected + established_y_corrected_j
        established_corrected_corrections = established_corrected_corrections + established_corrected_corrections_j
    established_y_corrected = np.asarray(established_y_corrected)
    established_corrected_correction_median_array = np.asarray(established_corrected_correction_median_array)
    established_corrected_corrections = np.asarray(established_corrected_corrections)

    established_x = []
    established_y = []
    established_x_bins = []
    established_median_array = []
    established_correction = []
    established_correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/file_template/phase='+str(phase_array[i])+'/phase_'+shaping+'_peaked/'
        Nloops = len(os.listdir(filedir))
        established_y_j = []
        established_x_j = []
        established_correction_j = []
        for j in range(Nloops):
            print('Established Uncorrected Files '+samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
            established_y_j.append(t_cross)
            established_x_j.append(-1*i*phase_time)
            established_correction_j.append(-1*i*phase_time - t_cross)
        established_median_array.append(np.median(np.asarray(established_y_j)))
        established_correction_median_array.append(np.median(np.asarray(established_correction_j)))
        established_y = established_y + established_y_j
        established_x = established_x + established_x_j
        established_correction = established_correction + established_correction_j
        established_x_bins.append(-1*(i-0.5)*phase_time)
    established_y = np.asarray(established_y)
    established_y = established_y - established_median_array[0]
    established_correction = np.asarray(established_correction)
    established_correction = established_correction + established_median_array[0]
    established_correction_median_array = np.asarray(established_correction_median_array)
    established_correction_median_array = established_correction_median_array + established_median_array[0]
    established_median_value = established_median_array[0]
    established_median_array = np.asarray(established_median_array)
    established_median_array = established_median_array - established_median_array[0]
    established_ybin = 1/(2*samplerate)
    established_y_bins = np.linspace(-2*established_ybin,0,num=maxphase,endpoint = True)
    established_y_bins_corrections = np.linspace(-established_ybin,established_ybin,num=maxphase,endpoint = True)
    established_x_bins = np.asarray(established_x_bins)
    established_x_bins = np.flip(established_x_bins)

    established_y_corrected = []
    established_corrected_median_array = []
    established_corrected_corrections = []
    established_corrected_correction_median_array = []
    for i in range(len(phase_array)):
        filedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/'+samplerate_name+'/file_template/phase='+str(phase_array[i])+'/phase_'+shaping+'_peaked/'
        Nloops = len(os.listdir(filedir))
        established_corrected_corrections_j = []
        established_y_corrected_j = []
        for j in range(Nloops):
            print('Established Corrected Files '+samplerate_name+';'+str(n_box)+','+str(n_delay)+','+str(n_att)+';'+str(i)+','+str(j))
            filename = filedir + 'Phase--waveforms--%05d.txt' % j
            (t,v,_) = rw(filename,numhead)
            t_avg,v_avg = boxcar_wf(t,v,n_box)
            v_delay = delay_wf(v_avg,n_delay)
            v_att = attenuate_wf(v_avg,n_att)
            v_sum = sum_wf(v_att,v_delay)
            t_cross,_,_ = zc_locator(t_avg,v_sum)
            established_t_corrected = t_cross - established_median_value + established_correction_median_array[i]
            established_y_corrected_j.append(established_t_corrected)
            established_corrected_correction = -1*i*phase_time - established_t_corrected
            established_corrected_corrections_j.append(established_corrected_correction)
        established_corrected_median_array.append(np.median(np.asarray(established_y_corrected_j)))
        established_corrected_correction_median_array.append(np.median(np.asarray(established_corrected_corrections_j)))
        established_y_corrected = established_y_corrected + established_y_corrected_j
        established_corrected_corrections = established_corrected_corrections + established_corrected_corrections_j
    established_y_corrected = np.asarray(established_y_corrected)
    established_corrected_correction_median_array = np.asarray(established_corrected_correction_median_array)
    established_corrected_corrections = np.asarray(established_corrected_corrections)

    savedir = 'G:/data/watchman/'+str(datadate)+'_watchman_spe/studies/phase/' + samplerate_name + '/array_data/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    np.savetxt(savedir+'x.csv', x, delimiter=',')
    np.savetxt(savedir+'y.csv', y, delimiter=',')
    np.savetxt(savedir+'x_bins.csv', x_bins, delimiter=',')
    np.savetxt(savedir+'y_bins.csv', y_bins, delimiter=',')
    np.savetxt(savedir+'median_array.csv', median_array, delimiter=',')
    np.savetxt(savedir+'correction.csv', correction, delimiter=',')
    np.savetxt(savedir+'y_bins_corrections.csv', y_bins_corrections, delimiter=',')
    np.savetxt(savedir+'correction_median_array.csv', correction_median_array, delimiter=',')
    np.savetxt(savedir+'y_corrected.csv', y_corrected, delimiter=',')
    np.savetxt(savedir+'corrected_median_array.csv', corrected_median_array, delimiter=',')
    np.savetxt(savedir+'corrected_corrections.csv', corrected_corrections, delimiter=',')
    np.savetxt(savedir+'corrected_correction_median_array.csv', corrected_correction_median_array, delimiter=',')

    np.savetxt(savedir+'established_x_noised.csv', established_x, delimiter=',')
    np.savetxt(savedir+'established_y_noised.csv', established_y, delimiter=',')
    np.savetxt(savedir+'established_x_bins_noised.csv', established_x_bins, delimiter=',')
    np.savetxt(savedir+'established_y_bins_noised.csv', established_y_bins, delimiter=',')
    np.savetxt(savedir+'established_median_array_noised.csv', established_median_array, delimiter=',')
    np.savetxt(savedir+'established_correction_noised.csv', established_correction, delimiter=',')
    np.savetxt(savedir+'established_y_bins_corrections_noised.csv', established_y_bins_corrections, delimiter=',')
    np.savetxt(savedir+'established_correction_median_array_noised.csv', established_correction_median_array, delimiter=',')
    np.savetxt(savedir+'established_y_corrected_noised.csv', established_y_corrected, delimiter=',')
    np.savetxt(savedir+'established_corrected_median_array_noised.csv', established_corrected_median_array, delimiter=',')
    np.savetxt(savedir+'established_corrected_corrections_noised.csv', established_corrected_corrections, delimiter=',')
    np.savetxt(savedir+'established_corrected_correction_median_array_noised.csv', established_corrected_correction_median_array, delimiter=',')

    np.savetxt(savedir+'established_x_peaked.csv', established_x, delimiter=',')
    np.savetxt(savedir+'established_y_peaked.csv', established_y, delimiter=',')
    np.savetxt(savedir+'established_x_bins_peaked.csv', established_x_bins, delimiter=',')
    np.savetxt(savedir+'established_y_bins_peaked.csv', established_y_bins, delimiter=',')
    np.savetxt(savedir+'established_median_array_peaked.csv', established_median_array, delimiter=',')
    np.savetxt(savedir+'established_correction_peaked.csv', established_correction, delimiter=',')
    np.savetxt(savedir+'established_y_bins_corrections_peaked.csv', established_y_bins_corrections, delimiter=',')
    np.savetxt(savedir+'established_correction_median_array_peaked.csv', established_correction_median_array, delimiter=',')
    np.savetxt(savedir+'established_y_corrected_peaked.csv', established_y_corrected, delimiter=',')
    np.savetxt(savedir+'established_corrected_median_array_peaked.csv', established_corrected_median_array, delimiter=',')
    np.savetxt(savedir+'established_corrected_corrections_peaked.csv', established_corrected_corrections, delimiter=',')
    np.savetxt(savedir+'established_corrected_correction_median_array_peaked.csv', established_corrected_correction_median_array, delimiter=',')

    return()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="phase_hist_gen",description="Generates 2D Histograms of timing resolution vs. phase.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    phase_array_gen(250000000,'250 Msps','raw_gained_analyzed',args.datadate,2,1,2,args.numhead)