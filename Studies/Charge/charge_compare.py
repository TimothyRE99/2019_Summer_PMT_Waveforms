#reads in charge files and runs comparison

#import necessary
import os
import numpy as np
from writehistogram import write_histogram as wh

#calculates error
def error_calc(charge_exact,charge_approx):
    numerate = abs(charge_exact - charge_approx)        #calculate numerator for percent error calculation
    error = str(numerate / charge_exact * 100)          #calculate percent error
    return(error)

#reads in charge values
def read_charge(filename):
    charge = np.array([])       #initialize charge array
    #read in charges from charge files
    fin = open(filename,'r')
    for line in fin:
        charge = np.append(charge, float(line.split(',')[0]))
    fin.close
    return(charge)

#call functions
def charge_compare(datadate,subfolder):
    #establish directories to read from and write to
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/charge/'
    writedir = filedir + 'errors/'
    #creates writing directory if it doesn't exist
    if not os.path.exists(writedir):
        os.makedirs(writedir)
    #establish names of txt files to read from and write to
    filename = filedir + subfolder + '_normal_charge.txt'
    filename_digitized = filedir + subfolder + '_digitized_charge.txt'
    writename = writedir + subfolder + '_error_hist.txt'
    #read in charge values
    charge = read_charge(filename)
    charge_digit = read_charge(filename_digitized)
    #cycle through charge histograms and calculate percent error
    for i in range(len(charge)):
        print('Filename: %05d' % i)
        error = error_calc(charge[i],charge_digit[i])
        wh(error,writename)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="charge compare",description="Calculates percent error in charge for original waveform digitized and digitized waveform with noise")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw_gained')
    args = parser.parse_args()

    charge_compare(args.datadate,args.subfolder)