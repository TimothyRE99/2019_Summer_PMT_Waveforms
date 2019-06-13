#opens waveform and plots it

#import necessary
import numpy as np
import matplotlib.pyplot as plt
from readwaveform import read_waveform as rw
from zcf_determine import zc_locator as locator
from timing_CFD import boxcar_wf as bcw
from timing_CFD import delay_wf as dlw
from timing_CFD import attenuate_wf as atw
import os

#plotting loop function
def plot_waveform(datadate,numhead,subfolder,n_box,n_delay,n_att):
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/ndelay='+str(n_delay)+'/natt='+str(n_att)+'/'+subfolder+'/'
    Nloops = len(os.listdir(filedir))
    for i in range(Nloops):
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        filename2 = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        print(filename)
        (t,v,_) = rw(filename,numhead)
        (t2,v2,_) = rw(filename2,numhead)
        t_box,v_box = bcw(t2,v2,n_box)
        v_top = atw(v_box,n_att)
        v_bott = dlw(v_box,n_delay)
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
        plt.title('D3--waveforms--%05d\nnbox= ' % i + str(n_box) + ' ndelay= ' + str(n_delay) + ' natt= ' + str(n_att) + '\nsubfolder = ' + subfolder + '\nCrossing Time = %05gs' % zcl)
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
    parser.add_argument('--n_delay',type=int,help='number of indices to delay base waveform',default = 1)
    parser.add_argument('--n_att',type=int,help='amount to attenuate inverted waveform by, must be base 2',default = 1)
    args = parser.parse_args()

    plot_waveform(args.datadate,args.numhead,args.subfolder,args.n_box,args.n_delay,args.n_att)