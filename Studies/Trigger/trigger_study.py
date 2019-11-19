#triggers at 1/3, 1/4, and 1/6 peak height and sees how many files get caught properly

#import necessary
from readwaveform import read_waveform as rw
import numpy as np
import os
import shutil
import scipy.integrate as integrate
from math import erfc
from bar_chart import bar_chart as bc
from determinepeakamplitude import determine as det

#checking probability of being outside threshold in one direction
def gauss_check(std,threshold,mean):
    num_of_stds = abs(threshold - mean) / std   #determines how many stds away from mean
    erfc_val = erfc(num_of_stds / np.sqrt(2))   #calculates complementary error function
    prob_happening = ((erfc_val) / 2)           #calculates probability of noise
    return prob_happening

#checking against 1/3 mean peak
def third_checker(datadate,numhead,mean,std_noise,subfolder,new_fsps,samplerate,mean_noise,std):
    threshold = mean / 3                        #establishes threshold
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/' + samplerate + '/d3_'+subfolder+'_analyzed/'))    #establishes number of files to cycle through
    for i in range(Nloops):
        print('File Number, One Third Peak = %05d' % i)     #prints what file you're on
        #establishes and creates directories if needed
        true_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/' + samplerate + '/third/'+subfolder+'/true_positives'
        false_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/' + samplerate + '/third/'+subfolder+'/false_negatives'
        if not os.path.exists(true_pos_dir):
            os.makedirs(true_pos_dir)
        if not os.path.exists(false_neg_dir):
            os.makedirs(false_neg_dir)
        #establishes file to read from and reads
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/' + samplerate + '/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        (_,v,_) = rw(filename,numhead)
        #flips and checks against threshold
        v = -1 * v
        v_peak = max(v)
        if v_peak >= threshold:
            shutil.copy2(filename,true_pos_dir)
        else:
            shutil.copy2(filename,false_neg_dir)
    true_positives = len(os.listdir(true_pos_dir))
    prob_happening_noise = gauss_check(std_noise,threshold,mean_noise)
    noise_rate = prob_happening_noise * new_fsps
    percent_above = 1 - gauss_check(std,threshold,mean)
    return(true_positives,Nloops,noise_rate,percent_above)

#checking against 1/4 mean peak
def fourth_checker(datadate,mean,std_noise,subfolder,new_fsps,samplerate,mean_noise,std):
    threshold = mean / 4                        #establishes threshold
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/' + samplerate + '/d3_'+subfolder+'_analyzed/'))    #establishes number of files to cycle through
    prob_happening_noise = gauss_check(std_noise,threshold,mean_noise)
    noise_rate = prob_happening_noise * new_fsps
    percent_above = 1 - gauss_check(std,threshold,mean)
    return(Nloops,noise_rate,percent_above)

#checking against 1/6 mean peak
def sixth_checker(datadate,mean,std_noise,subfolder,new_fsps,samplerate,mean_noise,std):
    threshold = mean / 6                        #establishes threshold
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/' + samplerate + '/d3_'+subfolder+'_analyzed/'))    #establishes number of files to cycle through
    prob_happening_noise = gauss_check(std_noise,threshold,mean_noise)
    noise_rate = prob_happening_noise * new_fsps
    percent_above = 1 - gauss_check(std,threshold,mean)
    return(Nloops,noise_rate,percent_above)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="generate zero files",description="Generates files filled with zeroes and then noised.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--mean_noise',type=float,help='mean peak bits of noise',default = 0)
    parser.add_argument('--std_noise',type=float,help = 'standard deviation for noise in bits',default = 3.3)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw_gained')
    parser.add_argument('--new_fsps',type=float,help = 'sample rate of digitizer',default = 1000000000.0)
    parser.add_argument('--samplerate',type = str,help = 'downsampled rate to analyze (1 Gsps, 500 Msps, 250 Msps, 125 Msps)',default = '1 Gsps')
    args = parser.parse_args()

    (mean,std) = det(args.datadate,args.numhead,args.subfolder,args.samplerate)

    (third_true_positives, third_Nloops, third_noise_rate, third_percent_above) = third_checker(args.datadate,args.numhead,mean,args.std_noise,args.subfolder,args.new_fsps,args.samplerate,args.mean_noise,std)
    (fourth_Nloops, fourth_noise_rate, fourth_percent_above) = fourth_checker(args.datadate,mean,args.std_noise,args.subfolder,args.new_fsps,args.samplerate,args.mean_noise,std)
    (sixth_Nloops, sixth_noise_rate, sixth_percent_above) = sixth_checker(args.datadate,mean,args.std_noise,args.subfolder,args.new_fsps,args.samplerate,args.mean_noise,std)

    print('One Third Mean Peak Gives:\n\t' + str(third_true_positives) + '/' + str(third_Nloops) + ' True Positives')
    print('One Third Mean Peak Gives: %05d Files Predicted' % int(third_percent_above*third_Nloops))
    print('One Fourth Mean Peak Gives: %05d Files Predicted' % int(fourth_percent_above*fourth_Nloops))
    print('One Sixth Mean Peak Gives: %05d Files Predicted' % int(sixth_percent_above*sixth_Nloops))

    dark_rate = ['%05g Hertz' % third_noise_rate, '%05g Hertz' % fourth_noise_rate, '%05g Hertz' % sixth_noise_rate]
    bars_true_pos = [int(third_percent_above*third_Nloops),int(fourth_percent_above*fourth_Nloops),int(sixth_percent_above*sixth_Nloops)]
    bars_false_neg = [third_Nloops - int(third_percent_above*third_Nloops),fourth_Nloops - int(fourth_percent_above*fourth_Nloops),sixth_Nloops - int(sixth_percent_above*sixth_Nloops)]

    bc(args.datadate,args.subfolder,dark_rate,args.samplerate,bars_true_pos,bars_false_neg)