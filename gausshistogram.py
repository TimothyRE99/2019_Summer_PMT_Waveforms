#read a histogram csv file and develop a Gaussian fit from it

#import necessary
import numpy as np

#run gaussian fit
def gauss_histogram(filename):
    histo = np.array([])                            #setting blank array
    fin = open(filename,'r')                        #opening appropriate histogram to read
    for line in fin:                                #cycling through lines of histogram file
        histo = np.append(histo, float(line.split(',')[0]))             #adding lines as floats to histo array
    histo = np.sort(histo)                                  #sorting histo array from least to greatest
    #splitting off array into upper and lower halves
    histo_low = np.array_split(histo,2)[0]
    histo_high = np.array_split(histo,2)[1]
    #determining median of each half (aka, 1st and 3rd quartiles)
    medi_low = np.median(histo_low)
    medi_high = np.median(histo_high)
    iqr = (medi_high - medi_low)                    #calculating inter-quartile range
    #calculating outlier thresholds
    out_low = (medi_low - 1.5*iqr)
    out_high = (medi_low + 1.5*iqr)
    histo_out_remove = histo[np.where((out_low <= histo) & (histo <= out_high))]    #creating new array with outliers removed
    #determining mean and std guesses for central data
    histo_mean = np.mean(histo_out_remove)
    histo_std = np.std(histo_out_remove)
    return (histo_mean,histo_std)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='gausshistogram', description='deriving mean and std of histograms')
    parser.add_argument('--filename',type = str,help = 'path to location',default = "G:/data/watchman/20190724_watchman_spe/d1/d1_histograms/10_jitter.txt")
    args = parser.parse_args()

    (histo_mean,histo_std) = gauss_histogram(args.filename)
    print(histo_mean)
    print(histo_std)