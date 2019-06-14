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
    filedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/timing/nbox='+str(n_box)+'/ndelay='+str(n_delay)+'/natt='+str(n_att)+'/'+subfolder+'/'        #establishes directory to read from
    Nloops = len(os.listdir(filedir))   #establishes length to cycle through file
    for i in range(Nloops):
        #creates file names and prints them
        filename = filedir + 'D3--waveforms--%05d.txt' % i
        filename2 = 'G:/data/watchman/'+datadate+'_watchman_spe/d3/d3_'+subfolder+'_analyzed/D3--waveforms--%05d.txt' % i
        print(filename)
        #takes in t and v values
        (t,v,_) = rw(filename,numhead)
        (t2,v2,_) = rw(filename2,numhead)
        #runs CFD on v values
        t_box,v_box = bcw(t2,v2,n_box)
        v_top = atw(v_box,n_att)
        v_bott = dlw(v_box,n_delay)
        (zcl,index_Cross,index_Peak) = locator(t,v)     #determines time of zero crossing
        plt.plot(t,v)   #plots CFD'd waveforms
        plt.plot(t_box,v_bott,color = 'green')  #plots original/delayed waveform
        plt.plot(t_box,v_top,color='purple')    #plots inverted/attenuated waveform
        #plots scatters of each index
        plt.scatter(t,v)
        plt.scatter(t_box,v_bott,color = 'green')
        plt.scatter(t_box,v_top,color='purple')
        plt.axhline(y=0,color='black')  #creates 0 axis
        plt.axvline(x=zcl,color='red')  #creates line at zero crossing time
        #plots index of peak and index used for crossing 0
        plt.plot(t[index_Cross],v[index_Cross],'x',color = 'orange')
        plt.plot(t[index_Peak],v[index_Peak],'x',color = 'yellow')
        #estabishes title and labels
        plt.title('D3--waveforms--%05d\nnbox= ' % i + str(n_box) + ' ndelay= ' + str(n_delay) + ' natt= ' + str(n_att) + '\nsubfolder = ' + subfolder + '\nCrossing Time = %05gs' % zcl)
        plt.xlabel('Time')
        plt.ylabel('Bits')
        #shows plot
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