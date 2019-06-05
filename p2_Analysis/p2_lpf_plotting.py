#graphs average waveforms at various steps of tau'ing

#import necessary
from matplotlib import pyplot as plt
from readwaveform import read_waveform as rw
import os

#plotting the waveforms
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d2/d2_raw')) - 1
for i in range(Nloops):
    print('File: %05d' % i)
    (t_single,v_single,_) = rw('g:/data/watchman/20190516_watchman_spe/d2/d2_raw/D2--waveforms--%05d.txt' % i,5)
    (t_double,v_double,_) = rw('g:/data/watchman/20190516_watchman_spe/d2/d2_rise_doubled/D2--waveforms--%05d.txt' % i,5)
    (t_quadruple,v_quadruple,_) = rw('g:/data/watchman/20190516_watchman_spe/d2/d2_rise_quadrupled/D2--waveforms--%05d.txt' % i,5)
    (t_octuple,v_octuple,_) = rw('g:/data/watchman/20190516_watchman_spe/d2/d2_rise_octupled/D2--waveforms--%05d.txt' % i,5)
    #fig = plt.figure(figsize=(6,4))
    plt.plot(t_single,v_single)
    plt.plot(t_double,v_double,color='red')
    plt.plot(t_quadruple,v_quadruple,color='green')
    plt.plot(t_octuple,v_octuple,color='purple')
    plt.show()
    #fig.savefig('G:/data/watchman/20190516_watchman_spe/d2/d2_images/average_lpfing_multiple.png',dpi = 2500)