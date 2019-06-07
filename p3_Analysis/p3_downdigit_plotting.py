#import necessary
from matplotlib import pyplot as plt
from readwaveform import read_waveform as rw
import numpy as np
import os

#plotting the waveforms
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d3/d3_raw_analyzed')) - 1
for i in range(Nloops):
    print('File: %05d' % i)
    (t_single,v_single,_) = rw('g:/data/watchman/20190516_watchman_spe/d3/d3_raw_analyzed/D3--waveforms--%05d.txt' % i,5)
    (t_double,v_double,_) = rw('g:/data/watchman/20190516_watchman_spe/d3/d3_rise_doubled_analyzed/D3--waveforms--%05d.txt' % i,5)
    (t_quadruple,v_quadruple,_) = rw('g:/data/watchman/20190516_watchman_spe/d3/d3_rise_quadrupled_analyzed/D3--waveforms--%05d.txt' % i,5)
    (t_octuple,v_octuple,_) = rw('g:/data/watchman/20190516_watchman_spe/d3/d3_rise_octupled_analyzed/D3--waveforms--%05d.txt' % i,5)
    #running risetime calculation
    #risetime_single = risetimes(t_single,v_single)
    #risetime_double = risetimes(t_double,v_double)
    #risetime_quadruple = risetimes(t_quadruple,v_quadruple)
    #risetime_octuple = risetimes(t_octuple,v_octuple)
    #fig = plt.figure(figsize=(6,4))
    plt.plot(t_single,-1*v_single)
    plt.plot(t_double,-1*v_double,color='red')
    plt.plot(t_quadruple,-1*v_quadruple,color='green')
    plt.plot(t_octuple,-1*v_octuple,color='purple')
    #printing risetimes as the title
    #plt.title('Single Risetime = %05g' % risetime_single + 's\nDouble Risetime = %05g' % risetime_double + 's\nQuadruple Risetime = %05g' % risetime_quadruple + 's\nOctuple Risetime = %05g' % risetime_octuple + 's')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
    #fig.savefig('G:/data/watchman/20190516_watchman_spe/d2/d2_images/average_lpfing_multiple.png',dpi = 2500)