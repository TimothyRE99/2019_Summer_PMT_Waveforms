#determines and records where the zero crossing time of CFD'd waveforms is

#import necessary
import os
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from gausshistogram import gauss_histogram as gh
from readhistogram import read_histogram as rh

#determining ZCL from t and v
def zc_locator(t,v,n_delay):
    stop_ind = 7 + n_delay
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

#running through CFD files to generate txt file to save ZCLs
def ZCF(datadate,numhead,subfolder,n_box,n_delay,n_att):
    #establishes file directory to read from and creates save directory if necessary
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/ndelay='+str(n_delay)+'/natt='+str(n_att)+'/'+subfolder+'/'
    if not os.path.exists(filedir + 'ZCF_data/'):
        os.makedirs(filedir + 'ZCF_data/')
    Nloops = len(os.listdir(filedir)) - 1       #establishes number of files to cycle through
    writename = filedir + 'ZCF_data/ZCLs.txt'   #establishes name of txt file to save to
    for i in range(Nloops):
        print("File: %05d, NBOX: " % i + str(n_box) + ", NDELAY: " + str(n_delay) + " , NATT: " + str(n_att))    #prints name of file
        #establishes file to read and takes in data
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        (t,v,_) = rw(filename,numhead)
        t_cross,_,_ = zc_locator(t,v,n_delay)   #locates zero crossing time
        wh(str(t_cross),writename)      #writes to zero crossing time histogram file
    #runs through process to read, create, and display histogram plot
    (histo_mean,histo_std) = gh(writename)
    savename = subfolder + "/zero_crossing_time_nbox=" + str(n_box) + "_ndelay=" + str(n_delay) + "_natt=" + str(n_att)
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/histogram_images/' + subfolder):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/histogram_images/' + subfolder + '/')
    rh(writename,"Seconds","Histogram of Zero Crossing Times",savename,datadate,histo_mean,histo_std)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="timing CFD",description="Applies CFD algorithm to prepare for ZCF.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 1)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'averages/raw')
    args = parser.parse_args()

    #cycles through each combination of n values
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
    #                        ZCF(args.datadate,args.numhead,args.subfolder,n_box,n_delay,n_att)
    ZCF(args.datadate,args.numhead,args.subfolder,2,1,2)