#determines and generates plot of average shape of waveform

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw
from writewaveform import write_waveform
import os

#Determining average shape
def determine_average_shape(datadate,numhead):
    Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_normalized'))
    writename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/average_shape.txt'
    for i in range(Nloops):
        print(i)
        filename = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_normalized/D1--waveforms--%05d.txt' % i
        (t,y,_) = rw(filename,numhead)
        #starting array if this is first file
        if i == 0:
            ysum = y
        #adding additional normalized files to the array index-wise
        else:
            ysum = np.add(ysum,y)
    yfinal = np.divide(ysum,Nloops)                 #diving array index-wise by number of files added
    header_name = "Average Waveform Shape"
    write_waveform(t,yfinal,writename,header_name)      #writing array to waveform file
    return (t,yfinal)

#Generate plot
def generate_average_shape_plot(datadate,numhead):
    (x,y) = determine_average_shape(datadate,numhead)  #gathering t and v information as x and y from above function
    fig = plt.figure(figsize=(6,4))                     #initializing figure image saving
    plt.plot(x,y)                           #plotting x vs y
    #setting plot labels
    plt.xlabel('Time')
    plt.ylabel('Ratio to Peak Height')
    plt.title('Average Wave Shape')
    plt.show()                              #show plot for confirmation
    #finalize plot saving
    fig.savefig('G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_histograms/average_shape.png',dpi = 300)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='determineaverageshape', description='determining and writing plot of average waveform shape')
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    args = parser.parse_args()

    generate_average_shape_plot(args.datadate,args.numhead)