#rename d1_raw files and move to new folder

#import necessary
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#moves files
def d1rename(datadate,numhead):
    files = os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_raw')          #creating list of files in d1_raw directory
    for i in range(len(files)):
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_raw/' + files[i]   #appending directory to filename values
        writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_renamed/D1--waveforms--%05d.txt' % i      #renaming files to correspond with position in directory and moving to new folder
        (t,y,header) = rw(filename,numhead)             #reading files from filename directory
        write_waveform(t,y,writename,header)            #writing files to writename directory

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='d1rename', description='Rename the data and move to new location')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    d1rename(args.datadate,args.numhead)