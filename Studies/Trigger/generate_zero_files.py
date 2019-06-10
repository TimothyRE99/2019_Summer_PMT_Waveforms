#generates files originally populated with zeroes than adds noise

#import necessary
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import numpy as np
import os

#adding noise
def noise(v,noise):
    noise_array = np.random.normal(loc=0.0, scale = noise, size = len(v))   #generating noise array
    v_final = np.add(v, noise_array)    #adding noise to digitized values
    v_final = v_final.astype(int)       #converting values to ints
    return(v_final)

#generating files of zero
def zeroes(datadate,numhead,noise):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_analyzed'))
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/zero_files'):
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/zero_files')
    for i in range(Nloops):
        reference_file = 'g:/data/watchman/20190516_watchman_spe/d3/d3_raw_analyzed/D3--waveforms--%05d.txt' % i
        writename = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/zero_files/Studies--waveforms--%05d.txt' % i
        (t,_,header) = rw(reference_file,numhead)
        length = len(t)
        v = np.zeros(length)
        v_final = noise(v,noise)
        write_waveform(t,v_final,writename,header)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="generate zero files",description="Generates files filled with zeroes and then noised.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument("--noise",type=float,help='bits of noise from digitizer',default=3.3)
    args = parser.parse_args()

    zeroes(args.datadate,args.numhead,args.noise)