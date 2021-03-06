#graphs average waveforms at various steps of tau'ing

#import necessary
from matplotlib import pyplot as plt
from readwaveform import read_waveform as rw
import numpy as np
import os

#calculating the risetimes
def risetimes(t,v):
    v_norm = v/min(v)                         #normalizing for ease of calculations
    #determining where 10% and 90% are located
    check10 = v_norm <= .1
    check90 = v_norm >= .9
    #converting to array of indices
    index10 = np.asarray([k for k, x in enumerate(check10) if x])
    index90 = np.asarray([k for k, x in enumerate(check90) if x])
    index_90 = int(index90[0])
    index10_removed = index10[np.where(index10 < index_90)]         #removing all values after 90% rise index
    index_10 = int(index10_removed[len(index10_removed)-1])               #turning last 10% rise index into int
    risetime = float(t[index_90] - t[index_10])                          #rise time is time at 90% - time at 10%
    return(risetime)

#plotting the waveforms
datadate = '20190724'
Nloops = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw')) - 1
if not os.path.exists('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_images/'):
    os.makedirs('G:/data/watchman/'+datadate+'_watchman_spe/d2/d2_images/')
plt.rcParams.update({'font.size': 14})
for i in range(Nloops):
    print('File: %05d' % i)
    (t_single,v_single,_) = rw('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_raw/D2--waveforms--%05d.txt' % i,5)
    (t_double,v_double,_) = rw('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_doubled_gained/D2--waveforms--%05d.txt' % i,5)
    (t_quadruple,v_quadruple,_) = rw('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_quadrupled_gained/D2--waveforms--%05d.txt' % i,5)
    (t_octuple,v_octuple,_) = rw('g:/data/watchman/'+datadate+'_watchman_spe/d2/d2_rise_octupled_gained/D2--waveforms--%05d.txt' % i,5)
    #running risetime calculation
    risetime_single = risetimes(t_single,v_single)
    risetime_double = risetimes(t_double,v_double)
    risetime_quadruple = risetimes(t_quadruple,v_quadruple)
    risetime_octuple = risetimes(t_octuple,v_octuple)
    #fig = plt.figure(figsize=(6,4))
    unshaped, = plt.plot(t_single,-1*v_single,label='Unshaped Waveform')
    doubled, = plt.plot(t_double,-1*v_double,color='red',label='Shaped to Double Risetime')
    quadrupled, = plt.plot(t_quadruple,-1*v_quadruple,color='green',label='Shaped to Quadrupled Risetime')
    octupled, = plt.plot(t_octuple,-1*v_octuple,color='purple',label='Shaped to Octupled Risetime')
    #printing risetimes as the title
    plt.xlabel('Time (s)')
    plt.ylabel('Volts')
    plt.title('Sample SPE Waveform After P2:\nWaveform %05d' % i) 
    plt.legend(handles=[unshaped,doubled,quadrupled,octupled])
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
    #fig.savefig('G:/data/watchman/20190516_watchman_spe/d2/d2_images/average_lpfing_multiple.png',dpi = 500)