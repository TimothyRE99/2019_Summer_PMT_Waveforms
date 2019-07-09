#reads a histogram csv and plots it as a log plot

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf
import os

#Read and display the data
def fit_function(x,B,mu,sigma):
    #funcion for a gaussian scaled by factor B
    return (B * (1/np.sqrt(2 * np.pi * sigma**2)) * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))

def read_histogram(filename, x_label, title, savename, datadate):
    histo = np.array([])            #initializing array
    fin = open(filename,'r')        #opening histogram txt file in read mode
    #appending values from histogram txt file to array in order
    for line in fin:
        histo = np.append(histo, float(line.split(',')[0]))
    fin.close
    histo_data, bins_data = np.histogram(histo, bins = 200)     #establishing histogram data
    binwidth = (bins_data[1] - bins_data[0])                    #determining bin width
    #determining bin centers
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    plt.bar(binscenters, histo_data, width=binwidth, log=True)        #plotting histogram
    #establishing plot labels
    plt.xlabel(x_label)
    plt.ylabel('Count')
    plt.get_current_fig_manager().window.showMaximized()        #maximizes plot
    plt.show()      #showing plot for confirmation

#For testing purposes
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="read histogram",description="read the histogram datafile.")
    parser.add_argument("--x_label",type=str,help='label of x axis',default='Seconds')
    parser.add_argument("--title",type=str,help="title of histogram",default='Histogram of 20-80 Rise Times')
    parser.add_argument("--filename",type=str,help="filename",default='G:\\Data\\watchman\\20190516_watchman_spe\\studies\\timing\\nbox=2\\ndelay=1\\natt=2\\raw_gained\\ZCF_data\\ZCLs.txt')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    args = parser.parse_args()
    read_histogram(args.filename,args.x_label,args.title,"20_80_rise_time",args.datadate)