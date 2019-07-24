#reads a histogram csv and plots it

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf
import os

#Read and display the data
def fit_function(x,B,mu,sigma):
    #funcion for a gaussian scaled by factor B
    return (B * (1/np.sqrt(2 * np.pi * sigma**2)) * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))

def read_histogram(filename, x_label, title, savename, datadate, histo_mean, histo_std):
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
    b_guess = (len(histo) * binwidth)   #using area approximation to guess at B value
    popt, _ = cf(fit_function,xdata = binscenters,ydata = histo_data, p0 = [b_guess,histo_mean,histo_std], maxfev = 10000)
    #establishing 5 significant figure versions of the mean and std from curve fit
    gauss_mean = '%s' % float('%.5g' % popt[1])
    gauss_std = '%s' % float('%.5g' % popt[2])
    x_values = np.linspace(popt[1] - 1.5*popt[2], popt[1] + 1.5*popt[2], 100000)    #creating 100,000 x values to map curvefit gaussian to
    fig = plt.figure(figsize=(6,4))                         #intializing saving the figure
    plt.bar(binscenters, histo_data, width=binwidth)        #plotting histogram
    plt.plot(x_values, fit_function(x_values, *popt), color='darkorange')   #plotting curve fit
    #establishing plot labels
    plt.xlabel(x_label)
    plt.ylabel('Count')
    plt.title(title+'\nGaussian Fit Values:\nMean = '+gauss_mean+' '+x_label+'\nStandard Deviation = '+gauss_std+' '+x_label)
    plt.get_current_fig_manager().window.showMaximized()        #maximizes plot
    plt.show(block=False)      #showing plot for confirmation
    plt.pause(2)
    plt.close()
    #finalizing plot saving
    savedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/histogram_images/'
    fig.savefig(savedir+savename+'_hist.png',dpi = 500)

#For testing purposes
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="read histogram",description="read the histogram datafile.")
    parser.add_argument("--x_label",type=str,help='label of x axis',default='Seconds')
    parser.add_argument("--title",type=str,help="title of histogram",default='Histogram of 20-80 Rise Times')
    parser.add_argument("--filename",type=str,help="filename",default='G:/data/watchman/20190724_watchman_spe/d1/d1_histograms/20_80_rise_time.txt')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190724')
    parser.add_argument('--histo_mean',type = float,help = 'mean of the histogram without outliers', default = 2.3890246551536875e-09)
    parser.add_argument('--histo_std',type = float,help = 'standard deviation of the histogram without outliers', default = 8.978658875273273e-11)
    args = parser.parse_args()
    read_histogram(args.filename,args.x_label,args.title,"20_80_rise_time",args.datadate,args.histo_mean,args.histo_std)