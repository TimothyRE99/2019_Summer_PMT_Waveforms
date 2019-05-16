#writing a waveform to a CSV file

#import necessary
import numpy as np

#Write the data
def write_waveform(x,y,filename,header):
    fileout = open(filename,'w')
    for entry in header:
        fileout.write(entry)
    for ix,iy in zip(x,y):
        line = '%.7E,%f\n' % (ix,iy)
        fileout.write(line)
    fileout.close()

#For testing
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="write waveform",description="write a waveform datafile.")
    parser.add_argument("--header",type=str,help='header string for the output file',default=['LECROYWaveRunner‘N,20113,Waveform\n', 'Segments,1,SegmentSize,4002\n', 'Segment,TrigTime,TimeSinceSegment1\n', '#1,14-May-2019 13:29:30,0                 \n', 'Time,Ampl\n'])
    parser.add_argument("--filename",type=str,help="filename",default="./C2--waveforms--00000.txt")
    args = parser.parse_args()
    x = range(1000)
    y = [np.random.normal(0,1.) for i in range(1000)]
    write_waveform(x,y,args.filename,args.header)