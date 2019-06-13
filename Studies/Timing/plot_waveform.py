#opens waveform and plots it

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw
from zcf_determine import zc_locator as locator
from timing_CFD import boxcar_wf as bcw
from timing_CFD import shift_wf as sw
from timing_CFD import multiply_wf as mpw
import os

#plotting loop function
def plot_waveform(datadate,numhead,subfolder,n_box,n_shift,n_mult):
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/nshift='+str(n_shift)+'/nmult='+str(n_mult)+'/'+subfolder+'/'
    Nloops = len(os.listdir(filedir))
    for i in range(Nloops):
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        filename2 = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        print(filename)
        (t,v,_) = rw(filename,numhead)
        (t2,v2,_) = rw(filename2,numhead)
        t_box,v_box = bcw(t2,v2,n_box)
        v_bott = mpw(v_box,n_mult)
        v_top = sw(v_box,n_shift)
        (zcl,index_Cross,index_Peak) = locator(t,v)
        plt.plot(t,v)
        plt.plot(t_box,v_bott,color = 'green')
        plt.plot(t_box,v_top,color='purple')
        plt.scatter(t,v)
        plt.scatter(t_box,v_bott,color = 'green')
        plt.scatter(t_box,v_top,color='purple')
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
    parser.add_argument('--n_box',type=int,help='n value for boxcar averager',default = 0)
    parser.add_argument('--n_shift',type=int,help='number of indices to shift inverted waveform',default = 1)
    parser.add_argument('--n_mult',type=int,help='amount to multiply base waveform by, must be power of 2',default = 1)
    args = parser.parse_args()

    plot_waveform(args.datadate,args.numhead,args.subfolder,args.n_box,args.n_shift,args.n_mult)