#import necessary
from matplotlib import pyplot as plt
from readwaveform import read_waveform as rw
import numpy as np
import os

#plotting the waveforms
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d3/d3_averages/raw/'))
for i in range(Nloops):
    print('File: %05d' % i)
    (t_single,v_single,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/d3_averages/raw/D3--waveforms--%05d.txt' % i,1)
    (t_double,v_double,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/d3_averages/rise_doubled/D3--waveforms--%05d.txt' % i,1)
    (t_quadruple,v_quadruple,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/d3_averages/rise_quadrupled/D3--waveforms--%05d.txt' % i,1)
    (t_octuple,v_octuple,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/d3_averages/rise_octupled/D3--waveforms--%05d.txt' % i,1)
    plt.plot(t_single,-1*v_single)
    plt.plot(t_double,-1*v_double,color='red')
    plt.plot(t_quadruple,-1*v_quadruple,color='green')
    plt.plot(t_octuple,-1*v_octuple,color='purple')
    plt.scatter(t_single,-1*v_single)
    plt.scatter(t_double,-1*v_double,color='red')
    plt.scatter(t_quadruple,-1*v_quadruple,color='green')
    plt.scatter(t_octuple,-1*v_octuple,color='purple')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()