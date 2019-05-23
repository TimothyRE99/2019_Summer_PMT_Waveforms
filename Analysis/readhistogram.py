#reads a histogram csv and plots it

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#Read and display the data
def read_histogram(filename, x_label, title, savename, data_date, histo_mean, histo_std):
    histo = np.array([])
    fin = open(filename,'r')
    for line in fin:
        histo = np.append(histo, float(line.split(',')[0]))
    x_axis = np.linspace(histo_mean - 4*histo_std, histo_mean + 4*histo_std, 1000)
    fig = plt.figure(figsize=(6,4))
    plt.plot(x_axis, norm.pdf(x_axis,histo_mean,histo_std), color = 'orange')
    plt.hist(histo, bins=250, density=True)                               #set histogram to divide contents into 50 bins
    plt.xlabel(x_label)                                     #set x-axis label
    plt.ylabel("count")                                     #set y-axis label
    plt.title(title+'\nGaussian Fit Values:\nMean = '+str(histo_mean)+' '+x_label+'\nStandard Deviation = '+str(histo_std)+' '+x_label) #set title
    plt.show()                                              #show plot
    fig.savefig('G:/data/watchman/'+data_date+'_watchman_spe/d1/d1_histograms/'+savename+'_hist.png',dpi = 300)

#For testing purposes
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="read histogram",description="read the histogram datafile.")
    parser.add_argument("--x_label",type=str,help='label of x axis',default='x-axis')
    parser.add_argument("--title",type=str,help="title of histogram",default='title')
    parser.add_argument("--filename",type=str,help="filename",default='C:/Users/Timothy/Desktop/Summer Work/Reference/signal_chain_studies/d1/rise_time.txt')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--histo_mean',type = float,help = 'mean of the histogram without outliers', default = 50.0)
    parser.add_argument('--histo_std',type = float,help = 'standard deviation of the histogram without outliers', default = 5.0)
    args = parser.parse_args()
    read_histogram(args.filename,args.x_label,args.title,"Test",args.data_date,args.histo_mean,args.histo_std)