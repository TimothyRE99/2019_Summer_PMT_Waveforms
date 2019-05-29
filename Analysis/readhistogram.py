#reads a histogram csv and plots it

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf

#Read and display the data
def fit_function(x,B,mu,sigma):
    return (B * (1/np.sqrt(2 * np.pi * sigma**2)) * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))

def read_histogram(filename, x_label, title, savename, data_date, histo_mean, histo_std):
    histo = np.array([])
    fin = open(filename,'r')
    for line in fin:
        histo = np.append(histo, float(line.split(',')[0]))
    histo_data, bins_data = np.histogram(histo, bins = 200)
    binwidth = (bins_data[1] - bins_data[0])
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    b_guess = (len(histo) * binwidth)
    histo_sorted = np.sort(histo)
    histo_center = histo_sorted[np.where(((histo_mean - 2*histo_std) <= histo_sorted) & (histo_sorted <= (histo_mean + 2*histo_std)))]
    new_bins = int((histo_center[len(histo_center)-1] - histo_center[0]) / binwidth)
    histo_data_center, bins_data_center = np.histogram(histo_center, bins = new_bins)
    binscenters_center = np.array([0.5 * (bins_data_center[i] + bins_data_center[i+1]) for i in range(len(bins_data_center)-1)])
    popt, _ = cf(fit_function,xdata = binscenters_center,ydata = histo_data_center, p0 = [b_guess,histo_mean,histo_std], maxfev = 10000)
    gauss_mean = '%s' % float('%.5g' % popt[1])
    gauss_std = '%s' % float('%.5g' % popt[2])
    x_values = np.linspace(popt[1] - 1.5*popt[2], popt[1] + 1.5*popt[2], 100000)
    fig = plt.figure(figsize=(6,4))
    plt.bar(binscenters, histo_data, width=binwidth)
    plt.plot(x_values, fit_function(x_values, *popt), color='darkorange')
    plt.xlabel(x_label)
    plt.ylabel('Count')
    plt.title(title+'\nGaussian Fit Values:\nMean = '+gauss_mean+' '+x_label+'\nStandard Deviation = '+gauss_std+' '+x_label)
    plt.show()
    fig.savefig('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/histogram_images/'+savename+'_hist.png',dpi = 500)

#For testing purposes
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="read histogram",description="read the histogram datafile.")
    parser.add_argument("--x_label",type=str,help='label of x axis',default='Seconds')
    parser.add_argument("--title",type=str,help="title of histogram",default='Histogram of 20-80 Rise Times')
    parser.add_argument("--filename",type=str,help="filename",default='G:/data/watchman/20190516_watchman_spe/d1/d1_histograms/20_80_rise_time.txt')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--histo_mean',type = float,help = 'mean of the histogram without outliers', default = 2.3890246551536875e-09)
    parser.add_argument('--histo_std',type = float,help = 'standard deviation of the histogram without outliers', default = 8.978658875273273e-11)
    args = parser.parse_args()
    read_histogram(args.filename,args.x_label,args.title,"20_80_rise_time",args.data_date,args.histo_mean,args.histo_std)