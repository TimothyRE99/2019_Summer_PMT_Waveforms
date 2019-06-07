#move data from final d1 folder to raw location in d23 folder with rename

#import necessary
import os
import shutil

#move and rename code
def p2_prelim(datadate):
    files = sorted(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes'))          #creating list of files in d1_final_spes directory
    for i in range(len(files)):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/' + files[i]   #determining source file path
        #determining destination file path based on context of file
        if filename == 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/d1_info.txt':
            writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/d1_info.txt'
        else:
            writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/D2--waveforms--%05d.txt' % i
        shutil.copy2(filename,writename)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='p2 prelim', description='moving files from d1 to d2')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    args = parser.parse_args()

    p2_prelim(args.datadate)