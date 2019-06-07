#Moving filtered files from d2 to d3

#import necessary
import os
import shutil

#moving files
def p2_prelim(datadate,noise):
    if noise == 0:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled/'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled/'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled/'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw/'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled/'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled/'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled/'
    else:
        filedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_noise=' + str(noise) + 'V/'
        filedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V/'
        filedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V/'
        filedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V/'
        writedir1 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_noise=' + str(noise) + 'V/'
        writedir2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled_noise=' + str(noise) + 'V/'
        writedir4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled_noise=' + str(noise) + 'V/'
        writedir8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled_noise=' + str(noise) + 'V/'
    files1 = sorted(os.listdir(filedir1))
    if not os.path.exists(writedir1):
        os.makedirs(writedir1)
    if not os.path.exists(writedir2):
        os.makedirs(writedir2)
    if not os.path.exists(writedir2):
        os.makedirs(writedir2)
    if not os.path.exists(writedir2):
        os.makedirs(writedir2)
    for i in range(len(files1)):
        print('Unfiltered File: %05d' % i)
        filename1 = filedir1 + files1[i]
        if files1[i] == 'd1_info.txt':
            writename1 = writedir1 + 'd2_info.txt'
        else:
            writename1 = writedir1 + 'D3--waveforms--%05d.txt' % i
        shutil.copy2(filename1,writename1)
    for i in range(len(files1) - 1):
        print('Filtered File: %05d' % i)
        filename2 = filedir2 + 'D2--waveforms--%05d.txt' % i
        filename4 = filedir4 + 'D2--waveforms--%05d.txt' % i
        filename8 = filedir8 + 'D2--waveforms--%05d.txt' % i
        writename2 = writedir2 + 'D3--waveforms--%05d.txt' % i
        writename4 = writedir4 + 'D3--waveforms--%05d.txt' % i
        writename8 = writedir8 + 'D3--waveforms--%05d.txt' % i
        shutil.copy2(filename2,writename2)
        shutil.copy2(filename4,writename4)
        shutil.copy2(filename8,writename8)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='p3 prelim', description='moving files from d2 to d3')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--noise',type = float,help = 'amount of noise in files you want to copy', default = 0)
    args = parser.parse_args()

    p2_prelim(args.datadate,args.noise)