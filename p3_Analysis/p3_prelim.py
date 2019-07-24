#Moving filtered files from d2 to d3

#import necessary
import os
import shutil

#moving files
def p2_prelim(datadate,noise,gain_noise,gain_factor_2,gain_factor_4,gain_factor_8):
    #setting up directories to read from and write to
    if noise == 0 and gain_noise == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled'
    elif gain_noise == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_noise=' + str(noise) + 'V'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_noise=' + str(noise) + 'V'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled_noise=' + str(noise) + 'V'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled_noise=' + str(noise) + 'V'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled_noise=' + str(noise) + 'V'
    elif noise == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_gain_noise=' + str(gain_noise) + 'V'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled_gain_noise=' + str(gain_noise) + 'V'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_gain_noise=' + str(gain_noise) + 'V'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled_gain_noise=' + str(gain_noise) + 'V'
    else:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled_gain_noise=' + str(gain_noise) + 'V_noise=' + str(noise) + 'V'
    if gain_factor_2 != 1 or gain_factor_4 != 1 or gain_factor_8:
        filedir1 = filedir1 + '_gained/'
        filedir2 = filedir2 + '_gained/'
        filedir4 = filedir4 + '_gained/'
        filedir8 = filedir8 + '_gained/'
        writedir1 = writedir1 + '_gained/'
        writedir2 = writedir2 + '_gained/'
        writedir4 = writedir4 + '_gained/'
        writedir8 = writedir8 + '_gained/'
    else:
        filedir1 = filedir1 + '/'
        filedir2 = filedir2 + '/'
        filedir4 = filedir4 + '/'
        filedir8 = filedir8 + '/'
        writedir1 = writedir1 + '/'
        writedir2 = writedir2 + '/'
        writedir4 = writedir4 + '/'
        writedir8 = writedir8 + '/'
    files1 = sorted(os.listdir(filedir1))           #creating and sorting list of files from raw directory to be able to take out the info file
    #creating paths if they don't exist
    if not os.path.exists(writedir1):
        os.makedirs(writedir1)
    if not os.path.exists(writedir2):
        os.makedirs(writedir2)
    if not os.path.exists(writedir4):
        os.makedirs(writedir4)
    if not os.path.exists(writedir8):
        os.makedirs(writedir8)
    #cycling through files in raw directory
    for i in range(len(files1)):
        print('Unfiltered File: %05d' % i)      #showing count of file being processed
        filename1 = filedir1 + files1[i]        #establishing name of file
        #taking out info file to prevent naming issues
        if files1[i] == 'd1_info.txt':
            writename1 = writedir1 + 'd2_info.txt'
        else:
            writename1 = writedir1 + 'D3--waveforms--%05d.txt' % i
        shutil.copy2(filename1,writename1)      #writing files to new directory
    for i in range(len(files1) - 1):
        print('Filtered File: %05d' % i)        #showing count of file being processed
        #establishing names of files
        filename2 = filedir2 + 'D2--waveforms--%05d.txt' % i
        filename4 = filedir4 + 'D2--waveforms--%05d.txt' % i
        filename8 = filedir8 + 'D2--waveforms--%05d.txt' % i
        #establishing names to write to
        writename2 = writedir2 + 'D3--waveforms--%05d.txt' % i
        writename4 = writedir4 + 'D3--waveforms--%05d.txt' % i
        writename8 = writedir8 + 'D3--waveforms--%05d.txt' % i
        #writing file to new directory
        shutil.copy2(filename2,writename2)
        shutil.copy2(filename4,writename4)
        shutil.copy2(filename8,writename8)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='p3 prelim', description='moving files from d2 to d3')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--noise',type = float,help = 'amount of noise in files you want to copy', default = 0)
    parser.add_argument("--gain_noise",type=float,help="standard deviation of noise gaussian for gain step",default=0)
    parser.add_argument("--gain_factor_2",type=float,help="Factor to multiply doubled by",default=3.5867418798)
    parser.add_argument("--gain_factor_4",type=float,help="Factor to multiply quadrupled by",default=4.52070370286)
    parser.add_argument("--gain_factor_8",type=float,help="Factor to multiply octupled by",default=8.09019004097)
    args = parser.parse_args()

    p2_prelim(args.datadate,args.noise,args.gain_noise,args.gain_factor_2,args.gain_factor_4,args.gain_factor_8)