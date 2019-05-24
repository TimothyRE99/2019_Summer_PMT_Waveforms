#reads a histogram csv and plots it

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit as cf

#Read and display the data
def fit_function(x,B,mu,sigma):
    return (B * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))

def read_histogram(filename, x_label, title, savename, data_date, histo_mean, histo_std):
    histo = np.array([])
    fin = open(filename,'r')
    for line in fin:
        histo = np.append(histo, float(line.split(',')[0]))
    histo_data, bins_data = np.histogram(histo, bins = 100)
    binscenters = np.array([0.5 * (bins_data[i] + bins_data[i+1]) for i in range(len(bins_data)-1)])
    x_values = np.linspace(histo_mean - 6*histo_std, histo_mean+6*histo_std, 100000)
    popt, _ = cf(fit_function,xdata = binscenters,ydata = histo_data, p0 = [10,histo_mean,histo_std])
    gauss_mean = '%s' % float('%.5g' % popt[1])
    gauss_std = '%s' % float('%.5g' % popt[2])
    fig = plt.figure(figsize=(6,4))
    plt.bar(binscenters, histo_data, width=bins_data[1] - bins_data[0])
    plt.plot(x_values, fit_function(x_values, *popt), color='darkorange')
    plt.xlabel(x_label)
    plt.ylabel('Count')
    plt.xlim(float(gauss_mean)-8*float(gauss_std),float(gauss_mean)+20*float(gauss_std))
    plt.title(title+'\nGaussian Fit Values:\nMean = '+gauss_mean+' '+x_label+'\nStandard Deviation = '+gauss_std+' '+x_label)
    plt.show()
    fig.savefig('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/'+savename+'_hist.png',dpi = 500)

#For testing purposes
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="read histogram",description="read the histogram datafile.")
    parser.add_argument("--x_label",type=str,help='label of x axis',default='Seconds')
    parser.add_argument("--title",type=str,help="title of histogram",default='Histogram of 20-80 Rise Times')
    parser.add_argument("--filename",type=str,help="filename",default='G:/data/watchman/20190516_watchman_spe/d1/d1_histograms/20_80_rise_time.txt')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--histo_mean',type = float,help = 'mean of the histogram without outliers', default = 2.3388931256128115e-09)
    parser.add_argument('--histo_std',type = float,help = 'standard deviation of the histogram without outliers', default = 8.978200114877416e-11)
    args = parser.parse_args()
    read_histogram(args.filename,args.x_label,args.title,"20_80_Rise",args.data_date,args.histo_mean,args.histo_std)