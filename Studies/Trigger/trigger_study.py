#triggers at 1/3, 1/4, and 1/6 peak height and sees how many files get caught properly

#import necessary
from readwaveform import read_waveform as rw
import numpy as np
import os
import shutil

#checking against 1/3 mean peak
def third_checker(datadate,numhead,mean,subfolder):
    threshold = mean / 3
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'))
    for i in range(Nloops):
        print(i)
        true_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/true_positives'
        false_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/false_positives'
        true_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/true_negatives'
        false_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/false_negatives'
        if not os.path.exists(true_pos_dir):
            os.makedirs(true_pos_dir)
        if not os.path.exists(false_pos_dir):
            os.makedirs(false_pos_dir)
        if not os.path.exists(true_neg_dir):
            os.makedirs(true_neg_dir)
        if not os.path.exists(false_neg_dir):
            os.makedirs(false_neg_dir)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        filename_zeroes = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/zero_files/Studies--waveforms--%05d.txt' % i
        (_,v,_) = rw(filename,numhead)
        (_,v_zeroes,_) = rw(filename_zeroes,numhead)
        v = -1 * v
        v_zeroes = -1 * v_zeroes
        v_peak = max(v)
        v_zeroes_peak = max(v_zeroes)
        if v_peak >= threshold:
            shutil.copy2(filename,true_pos_dir)
        else:
            shutil.copy2(filename,false_pos_dir)
        if v_zeroes_peak >= threshold:
            shutil.copy2(filename_zeroes,false_neg_dir)
        else:
            shutil.copy2(filename_zeroes,true_neg_dir)

#checking against 1/4 mean peak
def fourth_checker(datadate,numhead,mean,subfolder):
    threshold = mean / 4
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'))
    for i in range(Nloops):
        print(i)
        true_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/true_positives'
        false_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/false_positives'
        true_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/true_negatives'
        false_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/false_negatives'
        if not os.path.exists(true_pos_dir):
            os.makedirs(true_pos_dir)
        if not os.path.exists(false_pos_dir):
            os.makedirs(false_pos_dir)
        if not os.path.exists(true_neg_dir):
            os.makedirs(true_neg_dir)
        if not os.path.exists(false_neg_dir):
            os.makedirs(false_neg_dir)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        filename_zeroes = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/zero_files/Studies--waveforms--%05d.txt' % i
        (_,v,_) = rw(filename,numhead)
        (_,v_zeroes,_) = rw(filename_zeroes,numhead)
        v = -1 * v
        v_zeroes = -1 * v_zeroes
        v_peak = max(v)
        v_zeroes_peak = max(v_zeroes)
        if v_peak >= threshold:
            shutil.copy2(filename,true_pos_dir)
        else:
            shutil.copy2(filename,false_pos_dir)
        if v_zeroes_peak >= threshold:
            shutil.copy2(filename_zeroes,false_neg_dir)
        else:
            shutil.copy2(filename_zeroes,true_neg_dir)

#checking against 1/6 mean peak
def sixth_checker(datadate,numhead,mean,subfolder):
    threshold = mean / 6
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/'))
    for i in range(Nloops):
        print(i)
        true_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/true_positives'
        false_pos_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/false_positives'
        true_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/true_negatives'
        false_neg_dir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/false_negatives'
        if not os.path.exists(true_pos_dir):
            os.makedirs(true_pos_dir)
        if not os.path.exists(false_pos_dir):
            os.makedirs(false_pos_dir)
        if not os.path.exists(true_neg_dir):
            os.makedirs(true_neg_dir)
        if not os.path.exists(false_neg_dir):
            os.makedirs(false_neg_dir)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        filename_zeroes = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/zero_files/Studies--waveforms--%05d.txt' % i
        (_,v,_) = rw(filename,numhead)
        (_,v_zeroes,_) = rw(filename_zeroes,numhead)
        v = -1 * v
        v_zeroes = -1 * v_zeroes
        v_peak = max(v)
        v_zeroes_peak = max(v_zeroes)
        if v_peak >= threshold:
            shutil.copy2(filename,true_pos_dir)
        else:
            shutil.copy2(filename,false_pos_dir)
        if v_zeroes_peak >= threshold:
            shutil.copy2(filename_zeroes,false_neg_dir)
        else:
            shutil.copy2(filename_zeroes,true_neg_dir)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="generate zero files",description="Generates files filled with zeroes and then noised.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--mean',type=float,help='mean peak bits of waveform',default = 0.0)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw')
    args = parser.parse_args()

    third_checker(args.datadate,args.numhead,args.mean,args.subfolder)
    fourth_checker(args.datadate,args.numhead,args.mean,args.subfolder)
    sixth_checker(args.datadate,args.numhead,args.mean,args.subfolder)