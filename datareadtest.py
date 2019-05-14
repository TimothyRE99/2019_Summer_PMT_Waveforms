import csv
from itertools import islice

with open('g:/data/watchman/20190514_watchman_spe/C2--waveforms--00000.txt','r')as f:
    data = csv.reader(f)
    for row in islice(data, 10):
        print(row)