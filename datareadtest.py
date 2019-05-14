#import necessary
import csv
from itertools import islice

#setting variables
x = 0
results = []

#opening and printing data file
while x < 10:
    with open('g:/data/watchman/20190514_watchman_spe/C2--waveforms--0000'+str(x)+'.txt','r')as f:
        data = csv.reader(f)
        for row in islice(data, 10):
            results.append(row)
    print(results)
    print()
    results = []
    x += 1