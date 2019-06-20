#triggers at 1/3, 1/4, and 1/6 peak height and sees how many files get caught properly

#import necessary
from readwaveform import read_waveform as rw
import numpy as np
import os
import shutil
import scipy.integrate as integrate
from math import erfc
from bar_chart import bar_chart as bc

#checking how many times noise will register as SPE
def noise_check(std,threshold,new_fsps):
    num_of_stds = threshold / std               #determines how many stds away from mean
    erfc_val = erfc(num_of_stds / np.sqrt(2))   #calculates complementary error function
    prob_happening = ((erfc_val) / 2)           #calculates probability of noise
    noise_rate = prob_happening * new_fsps      #calculates noise rate
    return noise_rate

#checking against 1/3 mean peak
def third_checker(datadate,numhead,mean,std,subfolder,new_fsps):
    threshold = mean / 3                        #establishes threshold
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'))    #establishes number of files to cycle through
    for i in range(Nloops):
        print('File Number, One Third Peak = %05d' % i)     #prints what file you're on
        #establishes and creates directories if needed
        true_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/true_positives'
        false_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/false_negatives'
        if not os.path.exists(true_pos_dir):
            os.makedirs(true_pos_dir)
        if not os.path.exists(false_neg_dir):
            os.makedirs(false_neg_dir)
        #establishes file to read from and reads
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        (_,v,_) = rw(filename,numhead)
        #flips and checks against threshold
        v = -1 * v
        v_peak = max(v)
        if v_peak >= threshold:
            shutil.copy2(filename,true_pos_dir)
        else:
            shutil.copy2(filename,false_neg_dir)
    true_positives = len(os.listdir(true_pos_dir))
    noise_rate = noise_check(std,threshold,new_fsps)
    return(true_positives,Nloops,noise_rate)

#checking against 1/4 mean peak
def fourth_checker(datadate,numhead,mean,std,subfolder,new_fsps):
    threshold = mean / 4                        #establishes threshold
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'))    #establishes number of files to cycle through
    for i in range(Nloops):
        print('File Number, One Fourth Peak = %05d' % i)     #prints what file you're on
        #establishes and creates directories if needed
        true_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/true_positives'
        false_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/false_negatives'
        if not os.path.exists(true_pos_dir):
            os.makedirs(true_pos_dir)
        if not os.path.exists(false_neg_dir):
            os.makedirs(false_neg_dir)
        #establishes file to read from and reads
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        (_,v,_) = rw(filename,numhead)
        #flips and checks against threshold
        v = -1 * v
        v_peak = max(v)
        if v_peak >= threshold:
            shutil.copy2(filename,true_pos_dir)
        else:
            shutil.copy2(filename,false_neg_dir)
    true_positives = len(os.listdir(true_pos_dir))
    noise_rate = noise_check(std,threshold,new_fsps)
    return(true_positives,Nloops,noise_rate)

#checking against 1/6 mean peak
def sixth_checker(datadate,numhead,mean,std,subfolder,new_fsps):
    threshold = mean / 6                        #establishes threshold
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'))    #establishes number of files to cycle through
    for i in range(Nloops):
        print('File Number, One Sixth Peak = %05d' % i)     #prints what file you're on
        #establishes and creates directories if needed
        true_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/true_positives'
        false_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/false_negatives'
        if not os.path.exists(true_pos_dir):
            os.makedirs(true_pos_dir)
        if not os.path.exists(false_neg_dir):
            os.makedirs(false_neg_dir)
        #establishes file to read from and reads
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        (_,v,_) = rw(filename,numhead)
        #flips and checks against threshold
        v = -1 * v
        v_peak = max(v)
        if v_peak >= threshold:
            shutil.copy2(filename,true_pos_dir)
        else:
            shutil.copy2(filename,false_neg_dir)
    true_positives = len(os.listdir(true_pos_dir))
    noise_rate = noise_check(std,threshold,new_fsps)
    return(true_positives,Nloops,noise_rate)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="generate zero files",description="Generates files filled with zeroes and then noised.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--mean',type=float,help='mean peak bits of waveform',default = 204.84)
    parser.add_argument('--std',type=float,help = 'standard deviation for noise in bits',default = 3.3)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'rise_octupled_gained')
    parser.add_argument('--new_fsps',type=float,help = 'sample rate of digitizer',default = 250000000.0)
    args = parser.parse_args()

    (third_true_positives, third_Nloops, third_noise_rate) = third_checker(args.datadate,args.numhead,args.mean,args.std,args.subfolder,args.new_fsps)
    (fourth_true_positives, fourth_Nloops, fourth_noise_rate) = fourth_checker(args.datadate,args.numhead,args.mean,args.std,args.subfolder,args.new_fsps)
    (sixth_true_positives, sixth_Nloops, sixth_noise_rate) = sixth_checker(args.datadate,args.numhead,args.mean,args.std,args.subfolder,args.new_fsps)

    print('One Third Mean Peak Gives:\n\t' + str(third_true_positives) + '/' + str(third_Nloops) + ' True Positives')
    print('One Fourth Mean Peak Gives:\n\t' + str(fourth_true_positives) + '/' + str(fourth_Nloops) + ' True Positives')
    print('One Sixth Mean Peak Gives:\n\t' + str(sixth_true_positives) + '/' + str(sixth_Nloops) + ' True Positives')

    dark_rate = ['%05g Hertz' % third_noise_rate, '%05g Hertz' % fourth_noise_rate, '%05g Hertz' % sixth_noise_rate]

    bc(args.datadate,args.subfolder,dark_rate)