#Moving filtered files from d2 to d3

#import necessary
import os
import shutil

#moving files
def p2_prelim(datadate,noise):
    if noise == 0:
        files1 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/'))
        files2 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled/'))
        files4 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled/'))
        files8 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled/'))
    else:
        files1 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_noise=' + str(noise) + 'V/'))
        files2 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V/'))
        files4 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V/'))
        files8 = sorted(os.listdir('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V/'))
    for i in range(len(files1)):
        print('Unfiltered File: %05d' % i)
        if noise != 0:
            filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_noise=' + str(noise) + 'V/' + files1[i]
            if filename == 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw_noise=' + str(noise) + 'V/d1_info.txt':
                writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_noise=' + str(noise) + 'V/d2_info.txt'
            else:
                writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw_noise=' + str(noise) + 'V/D3--waveforms--%05d.txt' % i
        else:
            filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/' + files1[i]
            if filename == 'G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/d1_info.txt':
                writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw/d2_info.txt'
            else:
                writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_raw/D3--waveforms--%05d.txt' % i
        if not os.path.exists(writename):
            os.makedirs(writename.replace('D3--waveforms--%05d' % i, ''))
        shutil.copy2(filename,writename)
    for i in range(len(files2)):
        print('Filtered File: %05d' % i)
        if noise == 0:
            filename2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled/' + files2[i]
            filename4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled/' + files4[i]
            filename8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled/' + files8[i]
            writename2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_doubled/D3--waveforms--%05d.txt' % i
            writename4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_quadrupled/D3--waveforms--%05d.txt' % i
            writename8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d3/d3_rise_octupled/D3--waveforms--%05d.txt' % i
        else:
            filename2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V/' + files2[i]
            filename4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V/' + files4[i]
            filename8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V/' + files8[i]
            writename2 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_noise=' + str(noise) + 'V/D3--waveforms--%05d.txt' % i
            writename4 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_noise=' + str(noise) + 'V/D3--waveforms--%05d.txt' % i
            writename8 = 'g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_noise=' + str(noise) + 'V/D3--waveforms--%05d.txt' % i
        if not os.path.exists(writename2):
            os.makedirs(writename2.replace('D3--waveforms--%05d' % i, ''))
        if not os.path.exists(writename4):
            os.makedirs(writename4.replace('D3--waveforms--%05d' % i, ''))
        if not os.path.exists(writename8):
            os.makedirs(writename8.replace('D3--waveforms--%05d' % i, ''))
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