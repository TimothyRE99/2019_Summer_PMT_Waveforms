#determines and records where the zero crossing time of CFD'd waveforms is

#import necessary
import os
import numpy as np
from readwaveform import read_waveform as rw

def write_waveform(x,y,filename,header):
    fileout = open(filename,'w')
    #writing header data to file
    for entry in header:
        fileout.write(entry)
    #writing line data to file
    for ix,iy in zip(x,y):
        line = '%f,%f\n' % (ix,iy)
        fileout.write(line)
    fileout.close()

#determining ZCL from t and v
def zc_locator(t,v):
    v_norm = v/min(v)
    checkPeak = v_norm == 1
    checkCross = v_norm <= 0
    indexPeak = np.asarray([k for k, x in enumerate(checkPeak) if x])
    indexCross = np.asarray([k for k, x in enumerate(checkCross) if x])
    index_Peak = indexPeak[0]
    indexCross_removed = indexCross[np.where(indexCross < index_Peak)]
    index_Cross = indexCross_removed[len(indexCross_removed) - 1]
    t_bef = t[index_Cross]
    t_aft = t[index_Cross + 1]
    v_bef = v[index_Cross]
    v_aft = v[index_Cross + 1]
    slope = (v_aft - v_bef) / (t_aft - t_bef)
    t_pass = (-1 * v_bef) / slope
    t_cross = t_bef + t_pass
    return t_cross

#running through CFD files to generate txt file to save ZCLs
def ZCF(datadate,numhead,subfolder,n_box,n_shift,n_mult):
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'_nshift='+str(n_shift)+'_nmult='+str(n_mult)+'/'+subfolder+'/'
    if not os.path.exists(filedir + 'ZCF_data/'):
        os.makedirs(filedir + 'ZCF_data/')
    Nloops = len(os.listdir(filedir)) - 1
    file_list = np.array([])
    zcl_list = np.array([])
    for i in range(Nloops):
        print("File: %05d" % i)
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        (t,v,_) = rw(filename,numhead)
        t_cross = zc_locator(t,v)
        file_list = np.append(file_list, float('%05d' % i))
        zcl_list = np.append(zcl_list, t_cross)
    header = 'File Number, Zero Crossing Location'
    writename = filedir + 'ZCF_data/ZCLs.txt'
    write_waveform(file_list,zcl_list,writename,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="timing CFD",description="Applies CFD algorithm to prepare for ZCF.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw')
    parser.add_argument('--n_box',type=int,help='n value for boxcar averager',default = 0)
    parser.add_argument('--n_shift',type=int,help='number of indices to shift inverted waveform',default = 1)
    parser.add_argument('--n_mult',type=int,help='amount to multiply base waveform by, must be power of 2',default = 1)
    args = parser.parse_args()

    ZCF(args.datadate,args.numhead,args.subfolder,args.n_box,args.n_shift,args.n_mult)