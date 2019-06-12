#determines and records where the zero crossing time of CFD'd waveforms is

#import necessary
import os
import numpy as np
from readwaveform import read_waveform as rw
from writehistogram import write_histogram as wh
from gausshistogram import gauss_histogram as gh
from readhistogram import read_histogram as rh

#determining ZCL from t and v
def zc_locator(t,v):
    v_norm = v/min(v)
    checkPeak = v_norm == 1
    checkCross = v_norm <= 0
    indexPeak = np.asarray([k for k, x in enumerate(checkPeak) if x])
    indexCross = np.asarray([k for k, x in enumerate(checkCross) if x])
    index_Peak = indexPeak[0]
    indexCross_removed = indexCross[np.where(indexCross > index_Peak)]
    if len(indexCross_removed) == 0:
        t_cross = 'ALERT'
        print('Bad File!')
    else:
        index_Cross = indexCross_removed[0]
        t_bef = t[index_Cross - 1]
        t_aft = t[index_Cross]
        v_bef = v[index_Cross - 1]
        v_aft = v[index_Cross]
        slope = (v_aft - v_bef) / (t_aft - t_bef)
        t_pass = (-1 * v_bef) / slope
        t_cross = t_bef + t_pass
    return (t_cross,index_Cross,index_Peak)

#running through CFD files to generate txt file to save ZCLs
def ZCF(datadate,numhead,subfolder,n_box,n_shift,n_mult):
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/nshift='+str(n_shift)+'/nmult='+str(n_mult)+'/'+subfolder+'/'
    if not os.path.exists(filedir + 'ZCF_data/'):
        os.makedirs(filedir + 'ZCF_data/')
    Nloops = len(os.listdir(filedir)) - 1
    writename = filedir + 'ZCF_data/ZCLs.txt'
    for i in range(Nloops):
        print("File: %05d, NBOX: " % i + str(n_box) + ", NSHIFT:" + str(n_shift) + " , NMULT: " + str(n_mult))
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        (t,v,_) = rw(filename,numhead)
        t_cross,_,_ = zc_locator(t,v)
        wh(str(t_cross),writename)
    (histo_mean,histo_std) = gh(writename)
    savename = "zero_crossing_time_nbox:" + str(n_box) + "_nshift:" + str(n_shift) + "_nmult:" + str(n_mult)
    rh(writename,"Seconds","Histogram of 10-90 Fall Times",savename,datadate,histo_mean,histo_std)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="timing CFD",description="Applies CFD algorithm to prepare for ZCF.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw')
    args = parser.parse_args()

    for n_box in range(5):
        if n_box == 3:
            pass
        else:
            for n_shift in range(1,5):
                if n_shift == 3:
                    pass
                else:
                    for n_mult in range(1,5):
                        if n_mult == 3:
                            pass
                        else:
                            ZCF(args.datadate,args.numhead,args.subfolder,n_box,n_shift,n_mult)