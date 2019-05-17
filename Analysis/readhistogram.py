#reads a histogram csv and plots it

#import necessary
import csv
import numpy as np
import matplotlib.pyplot as plt

#Read and display the data
def read_histogram(filename, x_label, title):
    with open(filename, 'r') as my_file:                    #gather data from csv into list
        reader = csv.reader(my_file, delimiter = ',')
        histo = list(reader)
    plt.hist(histo, bins=50)                                #set histogram to divide contents into 50 bins
    plt.xlabel(x_label)                                     #set x-axis label
    plt.ylabel("count")                                     #set y-axis label
    plt.title(title)                                        #set title
    plt.show()                                              #show plot

#For testing purposes
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="read histogram",description="read the histogram datafile.")
    parser.add_argument("--x_label",type=str,help='label of x axis',default='x-axis')
    parser.add_argument("--title",type=str,help="title of histogram",default='title')
    parser.add_argument("--filename",type=str,help="filename",default='C:/Users/Timothy/Desktop/Summer Work/Reference/signal_chain_studies/d1/rise_time.txt')
    args = parser.parse_args()
    read_histogram(args.filename,args.x_label,args.title)