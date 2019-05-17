#Takes histogram data and writes it to a file

#Import necessary
import numpy as np
import os

#write the data
def write_histogram(value,filename):
    histogram = open(filename,"a")
    if os.stat(filename).st_size == 0:
        histogram.write(value)
    else:
        histogram.write(",\n"+value)
    histogram.close
    return

#testing
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="write histogram",description="write a histogram datafile.")
    parser.add_argument("--filename",type=str,help="filename",default="./C2--histograms.txt")
    args = parser.parse_args()
    length = np.random.randint(10,100)
    for i in range(length):
        value = str(i)
        write_histogram(value,args.filename)