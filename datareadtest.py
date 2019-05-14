#import necessary
import csv
from itertools import islice

#setting variables
counter = 0
print("Insert Number of Files Here:")
num_files = int(input())
print("Insert Number of Rows Here:")
num_rows = int(input())

#setting arrays
results = []

#opening and printing data file
while counter < num_files:
    with open('g:/data/watchman/20190514_watchman_spe/C2--waveforms--'+str(counter).zfill(5)+'.txt','r')as f:
        data = csv.reader(f)
        for row in islice(data, 4, num_rows):
            results.append(row)
    print(results)
    print()
    results = []
    counter += 1