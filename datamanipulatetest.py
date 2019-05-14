#import necessary
import csv
from itertools import islice

#setting variables
row_counter = 0
num_rows = 0
num_matches = 0
file_counter = 0

#setting arrays
results = []

#opening and printing data file
while file_counter < 1000:
    with open('g:/data/watchman/20190514_watchman_spe/C2--waveforms--'+str(file_counter).zfill(5)+'.txt','r')as f:
        data = csv.reader(f)
        for row in islice(data, 5, None):
            results.append(row)
    num_rows = len(results)
    while row_counter < num_rows:
        if float(results[row_counter][1]) <= -0.005:
            num_matches += 1
        row_counter += 1
    if num_matches > 0:
        print(num_matches)
        print(str(file_counter).zfill(5))
    num_matches = 0
    row_counter = 0
    results = []
    file_counter += 1
print("Done!")