#rename d1_raw files and move to new folder

#import necessary
import shutil
import os

#moves files
def d1rename(datadate):
    files = sorted(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_raw'))          #creating list of files in d1_raw directory
    if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_renamed/'): #creating directory for writing to if nonexistant
        os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_renamed/')
    for i in range(len(files)):
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_raw/' + files[i]   #appending directory to filename values
        writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_renamed/D1--waveforms--%05d.txt' % i      #renaming files to correspond with position in directory and moving to new folder
        shutil.copy2(filename,writename)    #copying files to new directory with new name

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='d1rename', description='Rename the data and move to new location')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    args = parser.parse_args()

    d1rename(args.datadate)