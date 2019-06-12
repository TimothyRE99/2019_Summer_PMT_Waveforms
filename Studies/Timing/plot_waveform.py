#opens waveform and plots it

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw
from zcf_determine import zc_locator as locator
import os

#plotting loop function
def plot_waveform(datadate,numhead,subfolder,n_box,n_shift,n_mult):
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/nshift='+str(n_shift)+'/nmult='+str(n_mult)+'/'+subfolder+'/'
    Nloops = len(os.listdir(filedir))
    for i in range(2414,Nloops):
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        print(filename)
        (t,v,_) = rw(filename,numhead)
        (zcl,index_Cross,index_Peak) = locator(t,v)
        plt.plot(t,v)
        plt.scatter(t,v)
        plt.axhline(y=0,color='black')
        plt.axvline(x=zcl,color='red')
        plt.plot(t[index_Cross],v[index_Cross],'x',color = 'orange')
        plt.plot(t[index_Peak],v[index_Peak],'x',color = 'yellow')
        plt.title('D3--waveforms--%05d\nnbox= ' % i + str(n_box) + ' nshift= ' + str(n_shift) + ' nmult= ' + str(n_mult) + '\nsubfolder = ' + subfolder + '\nCrossing Time = %05gs' % zcl)
        plt.xlabel('Time')
        plt.ylabel('Bits')
        plt.get_current_fig_manager().window.showMaximized()
        plt.show()

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="plot waveform",description="cycles through CFD waveforms and plots them.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--numhead',type=int,help='number of lines to ignore for header',default = 5)
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw')
    parser.add_argument('--n_box',type=int,help='n value for boxcar averager',default = 2)
    parser.add_argument('--n_shift',type=int,help='number of indices to shift inverted waveform',default = 1)
    parser.add_argument('--n_mult',type=int,help='amount to multiply base waveform by, must be power of 2',default = 4)
    args = parser.parse_args()

    plot_waveform(args.datadate,args.numhead,args.subfolder,args.n_box,args.n_shift,args.n_mult)