#import necessary
from matplotlib import pyplot as plt
from readwaveform import read_waveform as rw
import numpy as np
import os

#plotting the waveforms
Nloops = len(os.listdir('G:/data/watchman/20190516_watchman_spe/d3/500 Mhz/d3_averages/raw/'))
plt.rcParams.update({'font.size': 16})
for i in range(Nloops):
    print('File: %05d' % i)
    (t_single,v_single,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/500 Mhz/d3_averages/raw/D3--waveforms--%05d.txt' % i,1)
    (t_double,v_double,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/500 Mhz/d3_averages/rise_doubled/D3--waveforms--%05d.txt' % i,1)
    (t_quadruple,v_quadruple,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/500 Mhz/d3_averages/rise_quadrupled/D3--waveforms--%05d.txt' % i,1)
    (t_octuple,v_octuple,_) = rw('G:/Data/watchman/20190516_watchman_spe/d3/500 Mhz/d3_averages/rise_octupled/D3--waveforms--%05d.txt' % i,1)
    unshaped, = plt.plot(t_single,-1*v_single,label='Unshaped Waveform')
    doubled, = plt.plot(t_double,-1*v_double,color='red',label='Shaped to Double Risetime')
    quadrupled, = plt.plot(t_quadruple,-1*v_quadruple,color='green',label='Shaped to Quadrupled Risetime')
    octupled, = plt.plot(t_octuple,-1*v_octuple,color='purple',label='Shaped to Octupled Risetime')
    plt.scatter(t_single,-1*v_single)
    plt.scatter(t_double,-1*v_double,color='red')
    plt.scatter(t_quadruple,-1*v_quadruple,color='green')
    plt.scatter(t_octuple,-1*v_octuple,color='purple')
    plt.xlabel('Time (s)')
    plt.ylabel('Bits')
    plt.title('500 Msps\nSample SPE Waveform After P3:\nWaveform %05d' % i) 
    plt.legend(handles=[unshaped,doubled,quadrupled,octupled])
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()